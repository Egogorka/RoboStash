import io
import logging
import psycopg2
from collections import defaultdict

from interfaces.IEntry import IEntry
from model.Entry import Entry

from typing import List

import time
import csv


class PostgresLoader:
    def __init__(self, connection_params: dict):
        self.connect = psycopg2.connect(**connection_params)
        self.dicts = defaultdict(dict)
        self.request_type_dict = {}
        self.device_type_dict = {}
        self._initialized = False
        logging.info("PostgresLoader: __init__: выполнен.")

    def _init_dicts(self):
        self.request_type_dict = {
            'GET': 1, 'POST': 2, 'PUT': 3, 'DELETE': 4
        }

        self.device_type_dict = {
            'PC': 1, 'mobile': 2, 'tablet': 3, 'bot': 4, 'other': 5
        }

        with self.connect as conn:
            cur = conn.cursor()
            for table, key in [
                ('dim_ip', 'ip_address'),
                ('dim_api', 'path'),
                ('dim_protocol', 'name'),
                ('dim_referer', 'url'),
                ('dim_user_agent', 'ua')
            ]:
                cur.execute(f"SELECT id, {key} FROM {table}")
                self.dicts[table] = {v: k for k, v in cur.fetchall()}
                logging.info(f"PostgresLoader: _init_dicts: справочник {table} загружен. {len(self.dicts[table])} записей.")

            cur.execute("SELECT id, name FROM dim_request_type")
            for row in cur.fetchall():
                self.request_type_dict[row[1]] = row[0]

            cur.execute("SELECT id, name FROM dim_device_type")
            for row in cur.fetchall():
                self.device_type_dict[row[1]] = row[0]

    def _update_dicts_batch(self, table: str, key_column: str, values: set) -> None:
        start = time.time()
        values = {v for v in values if v is not None}
        existing_values = self.dicts.get(table, {})
        new_values = [v for v in values if v not in existing_values]
        if not new_values:
            return

        buffer = io.StringIO()
        for value in new_values:
            buffer.write(f"{value}\n")
        buffer.seek(0)

        with self.connect as conn:
            cur = conn.cursor()
            cur.copy_expert(f"""
                COPY {table} ({key_column}) FROM STDIN WITH CSV
            """, buffer)
            conn.commit()

            cur.execute(f"SELECT id, {key_column} FROM {table} WHERE {key_column} = ANY(%s)", (new_values,))
            self.dicts[table].update({v: k for k, v in cur.fetchall()})
        logging.info(f"PostgresLoader: update_dicts_batch: {table}: занял {time.time() - start:.3f} сек.")

    def _update_user_agents_batch(self, entries: list[IEntry]) -> None:
        start = time.time()
        new_user_agents = {}
        for entry in entries:
            ua = entry.ua
            if ua not in self.dicts['dim_user_agent'] and ua not in new_user_agents:
                parsed = entry.parsed_ua
                device_type_id = self.device_type_dict.get(parsed.device_type, None)
                new_user_agents[ua] = [
                    ua, parsed.device_brand, parsed.device_model,
                    parsed.os_family, parsed.os_version,
                    parsed.browser_family, parsed.browser_version,
                    device_type_id
                ]

        if new_user_agents:
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerows(new_user_agents.values())
            buffer.seek(0)

            with self.connect as conn:
                cur = conn.cursor()
                cur.copy_expert("""
                    COPY dim_user_agent (
                        ua, device_brand, device_model, os_family,
                        os_version, browser_family, browser_version, device_type_id
                    ) FROM STDIN WITH CSV
                """, buffer)
                conn.commit()

                cur.execute("SELECT id, ua FROM dim_user_agent WHERE ua = ANY(%s)", (list(new_user_agents.keys()),))
                self.dicts['dim_user_agent'].update({ua: _id for _id, ua in cur.fetchall()})

        logging.info(f"PostgresLoader: update_user_agents_batch: занял {time.time() - start:.3f} сек.")

    def _log_to_fact_csv(self, entries: list[Entry], batch_size: int = 10000):
        start = time.time()
        ip_addresses = {e.ip for e in entries if e.ip}
        apis = {e.api for e in entries if e.api}
        protocols = {e.protocol for e in entries if e.protocol}
        referers = {e.referer for e in entries if e.referer}

        self._update_dicts_batch('dim_ip', 'ip_address', ip_addresses)
        self._update_dicts_batch('dim_api', 'path', apis)
        self._update_dicts_batch('dim_protocol', 'name', protocols)
        self._update_dicts_batch('dim_referer', 'url', referers)
        self._update_user_agents_batch(entries)

        for e in entries:
            e.ip_id = self.dicts['dim_ip'].get(e.ip)
            e.api_id = self.dicts['dim_api'].get(e.api)
            e.protocol_id = self.dicts['dim_protocol'].get(e.protocol)
            e.referer_id = self.dicts['dim_referer'].get(e.referer)
            e.user_agent_id = self.dicts['dim_user_agent'].get(e.ua)
            e.request_type_id = self.request_type_dict.get(e.request_type)

        logging.info(f"PostgresLoader: load_log_batch: занял {time.time() - start:.3f} сек.")

    def _logs_to_csv_buffer(self, entries: List[Entry]) -> io.StringIO:
        start = time.time()
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        for e in entries:
            writer.writerow([
                e.ip_id, e.datetime, e.datetime.year, e.datetime.month, e.datetime.day,
                e.request_type_id, e.api_id, e.protocol_id, e.referer_id, e.user_agent_id,
                e.status_code, e.response_size, e.response_time,
                e.status_code >= 400, e.remote_user, e.user_id
            ])
        buffer.seek(0)
        logging.info(f"PostgresLoader: log_to_fact_csv: занял {time.time() - start:.3f} сек.")
        return buffer

    def _load_fact_log(self, buffer: io.StringIO):
        start = time.time()
        with self.connect as conn:
            cur = conn.cursor()
            cur.copy_expert("""
                COPY fact_logs (
                    ip_id, datetime, year, month, day,
                    request_type_id, api_id, protocol_id, referer_id, user_agent_id,
                    status_code, response_size, response_time, is_failed_request,
                    remote_user, user_id
                ) FROM STDIN WITH CSV
            """, buffer)
            conn.commit()
        logging.info(f"PostgresLoader: load_fact_log: занял {time.time() - start:.3f} сек.")

    def load_log(self, entries: list[IEntry], batch_size: int = 1000000):
        # one funny way to make lazy initialization
        if not self._initialized:
            self._init_dicts()
            logging.info("PostgresLoader: _init_dicts() выполнен.")
            self._initialized = True

        start_total = time.time()
        total_entries = len(entries)
        processed_entries = 0

        for i in range(0, total_entries, batch_size):
            batch = entries[i:i + batch_size]
            self._log_to_fact_csv(batch)
            buffer = self._logs_to_csv_buffer(batch)
            self._load_fact_log(buffer)

            processed_entries += len(batch)
            elapsed_time = time.time() - start_total
            speed = processed_entries / elapsed_time

            logging.info(
                f"PostgresLoader: load_log: {processed_entries}/{total_entries} записей. "
                f"Время: {elapsed_time:.2f} сек. Скорость: {speed:.2f} записей/сек."
            )

        total_time = time.time() - start_total
        logging.info(
            f"PostgresLoader: load_log: завершено за {total_time:.2f} сек. "
            f"Общая скорость: {processed_entries / total_time:.2f} записей/сек."
        )
