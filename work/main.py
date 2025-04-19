from db.postgresql.Database import Database  # путь к твоему классу Database
import os
import time
import logging
from Logging.Logging_configuration.logging_basic_config import set_basic_config

# Параметры подключения
db_config = {
    "dbname": "bd_logs",
    "user": "postgres",
    "password": "i8liveforChrist",
    "host": "localhost",
    "port": "5433"
}

# Папка с логами
log_dir = "./logs"

def main():
    # Настраимваем параметры логирования
    set_basic_config()

    # Создаём объект Database
    db = Database(connection_params=db_config)

    # Шаг 1: Инициализация таблиц
    db.create_tables(sql_files_directory="./sql_scripts/table")

    # Получаем список всех лог-файлов и сортируем (по имени файла)
    all_logs = sorted([
        f for f in os.listdir(log_dir)
        if f.endswith(".log")
    ])[:5]  # Только первые 5

    if not all_logs:
        logging.info("[!] В папке 'logs' нет лог-файлов.")
        return

    logging.info(f"[*] Найдено {len(all_logs)} лог-файлов. Загружаем первые 5:")

    for filename in all_logs:
        path = os.path.join(log_dir, filename)
        logging.info(f"[→] Загрузка: {path}")
        start = time.time()

        db.load_log(path)

        duration = time.time() - start
        logging.info(f"[✓] Файл '{filename}' загружен за {duration:.2f} сек.")

if __name__ == "__main__":
    main()
