from db.postgresql.Database import Database  # путь к твоему классу Database
import os
import time
#from  Logging.Logging_configuration.logging_basic_config import set_basic_config
import logging
class LogAnalyzerController:
    def db_load_result(self, result_message):
        # Обработка строки с результатами
        print(result_message)  # или другой код для обработки

# Пример вызова
c = LogAnalyzerController()
    # Параметры подключения к БД
db_config = {
    "dbname": "bd_logs",
    "user": "postgres",
    "password": "i8liveforChrist",
    "host": "localhost",
    "port": "5433"
}

def main():
    
    # Создаём директорию для CSV файлов, если её нет
    output_directory = './csv_files'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    


    # Создаем объект Database
    db = Database(connection_params=db_config, controller=c)

    # Получаем информацию о представлениях
    views = db.get_views_info()

    # Логируем доступные представления
    print("Доступные представления:")
    for view in views:
        print(view)

    # Сохраняем данные каждого представления в CSV
    for view_name in ["view_requests_by_ip_day", "view_count_requests_by_day", "view_top_ips", 
                      "view_count_ip_requests", "view_count_failed_requests_by_day", "view_count_status_code", 
                      "view_fact_logs"]:
        print(f"Получаем данные для представления: {view_name}")
        
        # Получаем данные для представления
        df = db.get_view_data(view_name)

        # Выводим названия полей
        field_names = df.columns.tolist()
        print(f"Названия полей для {view_name}: {', '.join(map(str, field_names))}")

        # Формируем имя файла для CSV
        csv_filename = os.path.join(output_directory, f"{view_name}.csv")

        # Сохраняем данные в CSV
        db.save_dict_to_csv(df.to_dict(orient='records'), csv_filename)
        print(f"Данные для представления {view_name} сохранены в файл {csv_filename}")

if __name__ == "__main__":
    #set_basic_config()
    main()
