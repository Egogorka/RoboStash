import io
import csv
import time

from parser.log_pr import open_logfile, get_all_logs, get_ua_list, ua_parser

class Parser:  # реализация класса загрузки в бд лога

    def nullify(self, value):
        return None if value=='-' else value

    def parse_logs(self, file_path):
        log_file = open_logfile(file_path)
        logs = get_all_logs(log_file)
        ua_list = get_ua_list(logs)
        parsed_ua_list = ua_parser(ua_list)
        return logs, parsed_ua_list

    def logs_to_csv_buffer(self, logs, parsed_ua_list):
        buffer = io.StringIO()
        writer = csv.writer(buffer)

        for log, ua in zip(logs, parsed_ua_list):
            writer.writerow([
                log[0], log[3], log[4], log[6], log[7], log[8],
                self.nullify(log[11]), log[12],
                self.nullify(ua[1]), self.nullify(ua[2]),
                self.nullify(ua[3]), self.nullify(ua[4]),
                self.nullify(ua[5]), self.nullify(ua[6]), self.nullify(ua[0]),
                log[9], log[10], log[13],
                self.nullify(log[1]), self.nullify(log[2])
            ])
        buffer.seek(0)
        return buffer

    def load_log(self, log_path: str):
        start_time = time.time()

        logs, parsed_ua = self.parse_logs(log_path)
        buffer = self.logs_to_csv_buffer(logs, parsed_ua)

        print(f"[✓] Загрузка '{log_path}' в буфер завершена за {time.time() - start_time:.2f} секунд.")
        return buffer
