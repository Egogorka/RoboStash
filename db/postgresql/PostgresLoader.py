import glob
import io
import csv
import time
from concurrent.futures import ThreadPoolExecutor

class PostgresLoader:  # реализация класса загрузки в бд лога
    def __init__(self, connect_function):
        self.connect = connect_function

    def _nullify(self, value):
        return None if value=='-' else value

    def _execute_sql_file(self, cursor, filename):
        with open(filename, "r", encoding='utf-8') as f:
            cursor.execute(f.read())

    def _parallel_insert_parts_from_file(self, sql_file_path, total_parts=10):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(self._insert_part_from_file, i, total_parts, sql_file_path)
                for i in range(total_parts)
            ]
            for future in futures:
                future.result()

    def _logs_to_csv_buffer(self, logs, parsed_ua_list):
        buffer = io.StringIO()
        writer = csv.writer(buffer)

        for log, ua in zip(logs, parsed_ua_list):
            writer.writerow([
                log[0], log[3], log[4], log[6], log[7], log[8],
                self._nullify(log[11]), log[12],
                self._nullify(ua[1]), self._nullify(ua[2]),
                self._nullify(ua[3]), self._nullify(ua[4]),
                self._nullify(ua[5]), self._nullify(ua[6]), self._nullify(ua[0]),
                log[9], log[10], log[13],
                self._nullify(log[1]), self._nullify(log[2])
            ])
        buffer.seek(0)
        return buffer

    def _load_to_staging_and_transfer(self, buffer):
        with self.connect() as conn:
            cur = conn.cursor()

            self._execute_sql_file(cur, "../sql_scripts/staging_logs/staging_logs_create.sql")

            copy_sql = """
                COPY staging_logs (
                    ip_address, date, t, request_type, api_path, protocol,
                    referer_url, ua, device_brand, device_model,
                    os_family, os_version, browser_family, browser_version,
                    device_type, status_code, response_size, response_time,
                    remote_user, user_id
                ) FROM STDIN WITH CSV
            """
            cur.copy_expert(copy_sql, buffer)
            conn.commit()

            insert_files = glob.glob('./sql_scripts/insert/insert_dim_*.sql')
            with ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(self._run_query_from_file, insert_files)

            self._parallel_insert_parts_from_file("../sql_scripts/insert/insert_fact_logs_parallel.sql", total_parts=10)

            self._execute_sql_file(cur, "../sql_scripts/staging_logs/staging_logs_delete.sql")
            conn.commit()

    def _insert_part_from_file(self, part, total, sql_file_path):
        with self.connect() as conn:
            with conn.cursor() as cur:
                with open(sql_file_path, 'r', encoding='utf-8') as f:
                    query = f.read().format(part=part, total=total)
                    cur.execute(query)
            conn.commit()
            print(f"[✔] Часть {part}/{total} завершена")

    def _run_query_from_file(self, file_path):
        with self.connect() as conn:
            with conn.cursor() as cur:
                with open(file_path, 'r', encoding='utf-8') as f:
                    query = f.read()
                    cur.execute(query)
            conn.commit()

    def load_log(self, logs, parsed_ua):
        print("Начинаю загрузку лога в БД")
        start_time = time.time()

        buffer = self._logs_to_csv_buffer(logs, parsed_ua)
        self._load_to_staging_and_transfer(buffer)

        print(f"[✓] Обработка лога завершена за {time.time() - start_time:.2f} секунд.")
