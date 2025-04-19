import time

from parser.log_pr import open_logfile, get_all_logs, get_ua_list, ua_parser

from interfaces.IParser import IParser, IEntry
from model.Entry import Entry, UserAgents

from typing import List
import logging

class Parser(IParser):

    def _parse_logs(self, file_path):
        log_file = open_logfile(file_path)
        logs = get_all_logs(log_file)
        ua_list = get_ua_list(logs)
        parsed_ua_list = ua_parser(ua_list)
        return logs, parsed_ua_list

    def parse(self, path: str) -> List[IEntry]:
        logging.info(f"Начинаем парсинг {path}")
        start_time = time.time()
        logs, parsed_ua_list = self._parse_logs(path)
        out = [Entry(log, parsed_ua) for log, parsed_ua in zip(logs, parsed_ua_list)]
        logging.info(f"[✓] Парсинг '{path}' завершён за {time.time() - start_time:.2f} секунд.")
        return out
