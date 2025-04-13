import psycopg2
import time
import io
import csv
from log_pr import open_logfile, get_all_logs, get_ua_list, ua_parser

def connect_to_db():
    return psycopg2.connect(
        dbname="bd_logs",
        user="postgres",
        password="i8liveforChrist",
        host="localhost",
        port="5433"
    )

def execute_sql_file(cursor, filename):
    print(f"📄 Executing {filename}...")
    with open(filename, "r") as f:
        cursor.execute(f.read())

def process_log_file(file_path):
    start_time = time.time()

    # Шаг 1: читаем и парсим логи
    log_file = open_logfile(file_path)
    logs = get_all_logs(log_file)
    print(f"📝 Parsed {len(logs)} logs in {time.time() - start_time:.2f} sec")

    # Шаг 2: разбираем user-agent
    ua_list = get_ua_list(logs)
    parsed_ua_list = ua_parser(ua_list)

    # Шаг 3: собираем данные в памяти в формате CSV
    start_time = time.time()
    buffer = io.StringIO()
    writer = csv.writer(buffer)

    for log, ua in zip(logs, parsed_ua_list):
        writer.writerow([
            log[0],             # ip_address
            log[3],             # date
            log[4],             # t (time)
            log[6],             # request_type
            log[7],             # api_path
            log[8],             # protocol
            log[11],            # referer_url
            log[12],            # ua
            ua[1],              # device_brand
            ua[2],              # device_model
            ua[3],              # os_family
            ua[4],              # os_version
            ua[5],              # browser_family
            ua[6],              # browser_version
            ua[0],              # device_type
            log[9],             # status_code
            log[10],            # response_size
            log[13],            # response_time
            log[1],             # remote_user
            log[2],             # user_id
        ])

    buffer.seek(0)
    print(f"📝 csv write logs in {time.time() - start_time:.2f} sec")

    # Шаг 4: вставка в staging_logs и перенос в fact_logs
    conn = connect_to_db()
    cursor = conn.cursor()

    # Создание staging таблицы
    execute_sql_file(cursor, "staging_logs_create.sql")

    # Загрузка данных
    start_time = time.time()
    copy_sql = """
        COPY staging_logs (
            ip_address, date, t,
            request_type, api_path, protocol,
            referer_url, ua, device_brand, device_model,
            os_family, os_version, browser_family, browser_version,
            device_type, status_code, response_size, response_time,
            remote_user, user_id
        ) FROM STDIN WITH CSV
    """
    cursor.copy_expert(copy_sql, buffer)
    conn.commit()
    print(f"✅ Data loaded to staging_logs in {time.time() - start_time:.2f} sec")

    # Добавление индексов
    execute_sql_file(cursor, "idx_staging_logs.sql")
    print("staging_logs: индексы добавлены")
    # Перенос данных в fact_logs
    execute_sql_file(cursor, "transfer_staging_to_fact.sql")
    print("staging_logs: fact_logs обновлен")
    # Удаление staging таблицы
    cursor.execute("DROP TABLE IF EXISTS staging_logs;")
    print("🧹 staging_logs удалена")

    conn.commit()
    cursor.close()
    conn.close()

# Запуск
process_log_file("logs/logfile1.log")
