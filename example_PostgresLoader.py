# main.py
import psycopg2
from PostgresLoader import PostgresLoader

# Функция подключения к базе данных
def connect_to_db():
    return psycopg2.connect(
        dbname="bd_logs",
        user="postgres",
        password="---",
        host="localhost",
        port="5433"
    )

# Путь к лог-файлу
log_file_path = "./logs/logfile1.log"

# Создаём объект загрузчика и загружаем лог
loader = PostgresLoader(connect_function=connect_to_db)
loader.load_log(log_file_path)
