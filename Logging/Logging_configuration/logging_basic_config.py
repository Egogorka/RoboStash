import os
import logging

def set_basic_config() -> None:
    log_dir = "./Logging/Logging_info"
    log_file = "logging_info.log"
    full_log_path = os.path.join(log_dir, log_file)
    
    # Создание директории, если не существует
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"[i] Создана директория: {log_dir}")
    
    # Настройка логирования для информационных сообщений
    logging.basicConfig(
        level=logging.INFO,
        filename=full_log_path,
        filemode='w',
        format="%(asctime)s %(levelname)s %(message)s"
    )
    
    # Создание обработчика для логирования ошибок
    log_dir = "./Logging/Logging_error"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"[i] Создана директория: {log_dir}")
    error_log_file = os.path.join(log_dir, "error_log.log")
    error_handler = logging.FileHandler(error_log_file)
    error_handler.setLevel(logging.ERROR)  # Логирование ошибок
    error_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))

    # Добавление обработчика ошибок в глобальный логгер
    logger = logging.getLogger()
    logger.addHandler(error_handler)

    print(f"[✓] Логгирование настроено: {full_log_path}")
    print(f"[✓] Логирование ошибок настроено: {error_log_file}")

