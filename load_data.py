import psycopg2
from log_pr import open_logfile, get_all_logs, get_ua_list, ua_parser
from user_agents import parse
import re
import time

def connect_to_db():
    """Подключение к базе данных PostgreSQL."""
    try:
        conn = psycopg2.connect(
            dbname="bd_logs", 
            user="postgres", 
            password="password", 
            host="localhost", 
            port="5432"
        )
        return conn
    except Exception as e:
        print("Connection failed:", e)

def insert_ip(conn, ip_address):
    """Вставка IP-адреса в таблицу dim_ip, если его нет."""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM dim_ip WHERE ip_address = %s", (ip_address,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO dim_ip (ip_address) VALUES (%s) RETURNING id", (ip_address,))
        conn.commit()
        return cursor.fetchone()[0]
    return result[0]

def insert_request_type(conn, request_type):
    """Вставка типа запроса в таблицу dim_request_type."""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM dim_request_type WHERE name = %s", (request_type,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO dim_request_type (name) VALUES (%s) RETURNING id", (request_type,))
        conn.commit()
        return cursor.fetchone()[0]
    return result[0]

def insert_api(conn, api_path):
    """Вставка пути API в таблицу dim_api."""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM dim_api WHERE path = %s", (api_path,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO dim_api (path) VALUES (%s) RETURNING id", (api_path,))
        conn.commit()
        return cursor.fetchone()[0]
    return result[0]

def insert_protocol(conn, protocol):
    """Вставка протокола в таблицу dim_protocol."""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM dim_protocol WHERE name = %s", (protocol,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO dim_protocol (name) VALUES (%s) RETURNING id", (protocol,))
        conn.commit()
        return cursor.fetchone()[0]
    return result[0]

def insert_referer(conn, referer):
    """Вставка реферера в таблицу dim_referer, если его нет, или оставление NULL."""
    if not referer:  # Если referer пустой или None, возвращаем NULL
        return None
    
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM dim_referer WHERE url = %s", (referer,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO dim_referer (url) VALUES (%s) RETURNING id", (referer,))
        conn.commit()
        return cursor.fetchone()[0]
    return result[0]

def insert_device_type(conn, device_type):
    """Вставка типа устройства в таблицу dim_device_type."""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM dim_device_type WHERE name = %s", (device_type,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO dim_device_type (name) VALUES (%s) RETURNING id", (device_type,))
        conn.commit()
        return cursor.fetchone()[0]
    return result[0]

def insert_user_agent(conn, ua_string, parsed_ua_list, device_type_id):
    device_type = parsed_ua_list[0]
    device_brand = parsed_ua_list[1]  if parsed_ua_list[1] != "-" else None
    device_model = parsed_ua_list[2] if parsed_ua_list[2] != "-" else None
    os_family = parsed_ua_list[3]
    os_version = parsed_ua_list[4]
    browser_family = parsed_ua_list[5]
    browser_version = parsed_ua_list[6]
    """Вставка строк пользовательского агента в таблицу dim_user_agent."""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM dim_user_agent WHERE ua = %s", (ua_string,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("""
        INSERT INTO dim_user_agent (ua, device_type_id, device_brand, device_model, os_family, os_version, browser_family, browser_version)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (ua_string, device_type_id, device_brand, device_model, os_family, os_version, browser_family, browser_version))
        conn.commit()
        return cursor.fetchone()[0]
    return result[0]

def insert_log_entry(conn, log_data):
    """Вставка записи лога в таблицу fact_logs."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO fact_logs (
            ip_id, date, year, month, t, 
            request_type_id, api_id, protocol_id, 
            referer_id, user_agent_id, 
            status_code, response_size, 
            response_time, is_failed_request,
            remote_user, user_id
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, log_data)
    conn.commit()

def process_log_file(file_path):
    """Обработка лог-файла и загрузка данных в БД."""
    # Чтение и парсинг лога
    log_file = open_logfile(file_path)
    print("\nopen_logfile\n")
    logs = get_all_logs(log_file)
    print("\nget_all_logs\n")
    ua_list = get_ua_list(logs)
    print("\nget_ua_list\n")
    parsed_ua_list = ua_parser(ua_list)
    print("\nua_parser\n")
    print(f"\nall_logs:{len(logs)}\n")

    # Подключаемся к базе данных
    conn = connect_to_db()
    processed_logs = 0
    start_time =time.time()
    total_logs=len(logs)
    # Обрабатываем каждую строку лога
    for log in logs:
        ip_address = log[0]
        remote_user = log[1] if log[1] != "-" else None
        user_id = log[2] if log[2] != "-" else None
        date = log[3]
        request_time = log[4]
        request_type = log[6]
        api_path = log[7]
        protocol = log[8]
        status_code = int(log[9])  # Преобразуем статус код в целое число
        response_size = int(log[10])  # Преобразуем размер ответа в целое число
        referer = log[11] 
        ua_string = log[12]

        # Вставляем данные в таблицы
        ip_id = insert_ip(conn, ip_address)
        request_type_id = insert_request_type(conn, request_type)
        api_id = insert_api(conn, api_path)
        protocol_id = insert_protocol(conn, protocol)
        if referer != "-":
            referer_id = insert_referer(conn, referer)
        else:
            referer_id = None
        # Извлекаем информацию о пользовательском агенте
        p = parsed_ua_list[logs.index(log)]
        device_type = p[0]
        
        device_type_id = insert_device_type(conn, device_type)
        user_agent_id = insert_user_agent(conn, ua_string, p, device_type_id)

        # Формируем данные для записи в таблицу fact_logs
        log_data = (
            ip_id, date, int(date.split("-")[0]), int(date.split("-")[1]), request_time,
            request_type_id, api_id, protocol_id, referer_id, user_agent_id,
            status_code, response_size, log[13], status_code >= 400, remote_user, user_id
        )

        # Вставляем запись в fact_logs
        insert_log_entry(conn, log_data)

        # Обновляем прогресс каждые 10 секунд и рассчитываем скорость
        processed_logs += 1
        elapsed_time = time.time() - start_time

        if elapsed_time >= 10:
            progress = (processed_logs / total_logs) * 100
            # Рассчитываем скорость загрузки (логи в секунду)
            print(f"Progress: {progress:.2f}%")
            start_time = time.time()  # сбрасываем таймер

    conn.close()

# Запуск процесса обработки логов
process_log_file("logs/logfile1.log")

