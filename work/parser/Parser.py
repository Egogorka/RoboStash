import time
import logging

from parser.log_pr import open_logfile, get_all_logs, get_ua_list, ua_parser
from interfaces.IParser import IParser, IEntry
from model.Entry import Entry
from typing import List


class Parser(IParser):
    def _parse_logs(self, file_path):
        start_total = time.time()

        start = time.time()
        log_file = open_logfile(file_path)
        logging.info(f"Parser: _parse_logs: Открытие файла логов заняло {time.time() - start:.3f} сек.")

        start = time.time()
        logs = get_all_logs(log_file)
        logging.info(f"Parser: _parse_logs: Извлечение логов заняло {time.time() - start:.3f} сек.")

        start = time.time()
        ua_list = get_ua_list(logs)
        logging.info(f"Parser: _parse_logs: Извлечение user-agent'ов заняло {time.time() - start:.3f} сек.")

        start = time.time()
        parsed_ua_list = ua_parser(ua_list)
        logging.info(f"Parser: _parse_logs: Парсинг user-agent'ов занял {time.time() - start:.3f} сек.")

        logging.info(f"Parser: _parse_logs: Завершено. Всего логов: {len(logs)}. Общее время: {time.time() - start_total:.3f} сек.")
        return logs, parsed_ua_list

    def parse(self, path: str) -> List[IEntry]:
        logging.info(f"Parser: parse: Начинаем парсинг файла {path}")
        start_time = time.time()

        logs, parsed_ua_list = self._parse_logs(path)
        out = [Entry(log, parsed_ua) for log, parsed_ua in zip(logs, parsed_ua_list)]

        elapsed = time.time() - start_time
        logging.info(f"Parser: parse: Парсинг '{path}' завершён за {elapsed:.3f} сек. Записей: {len(out)}")

        return out
