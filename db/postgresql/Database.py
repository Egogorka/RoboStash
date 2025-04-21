import psycopg2
import glob
import pandas as pd
import time
import logging
from sqlalchemy import create_engine

from interfaces.IDatabase import IDatabase
from db.postgresql.PostgresLoader import PostgresLoader

from typing import List
from interfaces.IEntry import IEntry


class Database(IDatabase):
    def __init__(self, connection_params):
        self.connection_params = connection_params
        self.loader = PostgresLoader(self._connection_args())

        # Создаем строку подключения для SQLAlchemy
        user = self.connection_params['user']
        password = self.connection_params['password']
        host = self.connection_params['host']
        port = self.connection_params['port']
        dbname = self.connection_params['dbname']

        self.engine = create_engine(
            f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'
        )



    def _connection_args(self):
        return {
            "user": self.connection_params['user'],
            "password": self.connection_params['password'],
            "host": self.connection_params['host'],
            "port": self.connection_params['port'],
            "dbname": self.connection_params['dbname'],
        }

    def _connect(self):
        self.conn = psycopg2.connect(**self._connection_args())
        self.cursor = self.conn.cursor()

    def _close(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    def create_tables(self, sql_files_directory='./sql_scripts/table'):
        self.execute_sql_files_directory(sql_files_directory)

    def get_views_info(self) -> dict:
        """
        Возвращает словарь представлений и их описаний из комментариев в базе данных.
        """
        self._connect()
        try:
            self.cursor.execute("""
                SELECT
                    c.relname AS view_name,
                    d.description AS view_description
                FROM pg_class c
                JOIN pg_namespace n ON n.oid = c.relnamespace
                LEFT JOIN pg_description d ON d.objoid = c.oid AND d.objsubid = 0
                WHERE c.relkind = 'v' AND n.nspname = 'public'
            """)
            results = self.cursor.fetchall()

            views_description = {
                view_name: description if description else view_name
                for view_name, description in results
            }

            return views_description

        finally:
            self._close()

    @staticmethod
    def get_views_info_old(self) -> dict:
        """
        Возвращает словарь доступных представлений с описаниями (без обращения к БД).
        """
        views_description = {
            "view_requests_by_ip_day": "Количество запросов и отказов по каждому IP и дню.",
            "view_count_requests_by_day": "Общее количество запросов по каждому дню.",
            "view_top_ips": "Топ IP-адресов по количеству запросов.",
            "view_count_ip_requests": "Сводная информация по IP-адресу: протокол, устройство, браузер и т.д.",
            "view_count_failed_requests_by_day": "Количество неуспешных запросов (ошибок) по дням.",
            "view_count_status_code": "Частота встречаемости различных HTTP-статусов.",
            "view_fact_logs": "Полное представление логов с расшифровкой связанных справочников: IP, user-agent, протоколы, API и прочее."
        }
        return views_description

    def create_views(self, sql_files_directory='./sql_scripts/views'):
        self.execute_sql_files_directory(sql_files_directory)

    def load_log(self, log_path: str):
        if not hasattr(self, 'loader'):
            self.loader = PostgresLoader(self.connection_params)
        p = Parser()
        start = time.time()
        
        # Загрузка лога
        self.loader.load_log(p.parse(log_path))
        
        end = time.time()
        
        # Формируем строку с результатами
        result_message = f"Загрузка лог-файла {log_path} завершена за {end - start:.2f} секунд"
        
        # Передаем результат в контроллер
        self.controller.db_load_result(result_message)
        
        logging.info(f"Database: load_log: Загрузка лога завершена за {end - start:.2f} секунд")

    def get_view_data(self, view_name: str, top_n: int = None) -> pd.DataFrame:
        query = f"SELECT * FROM {view_name}"
        if top_n is not None:
            query += f" LIMIT {top_n}"
        df = pd.read_sql_query(query, self.engine)
        if view_name == "view_requests_by_ip_day":
            return self.get_requests_by_ip_and_date(df)
        return df

    @staticmethod
    def save_dict_to_parquet(data: list[dict], filename: str):
        """
        Сохраняет данные в формате Parquet.
        """
        df = pd.DataFrame(data)
        df.to_parquet(filename, index=False, engine='pyarrow')
        logging.info(f"Database: Данные сохранены в файл: {filename} в формате Parquet")

    @staticmethod
    def save_dict_to_csv(data: list[dict], filename: str):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, sep=",", encoding='utf-8')
        logging.info(f"Database: Данные сохранены в файл: {filename}")


    @staticmethod
    def get_requests_by_ip_and_date(df: pd.DataFrame) -> pd.DataFrame:
        """
        Возвращает сводную таблицу: IP в строках, даты в столбцах, значения — количество запросов.
        """
        pivot_df = df.pivot_table(
            index='ip_address',     # строки — IP-адреса
            columns='date',         # столбцы — даты
            values='count',         # значения — количество запросов
            fill_value=0            # если нет данных — 0
        )
        return pivot_df

    def execute_sql_files_directory(self, sql_files_directory):
        self._connect()
        try:
            view_files = glob.glob(f"{sql_files_directory}/*.sql")
            if not view_files:
                logging.info(f"Database: Нет SQL-файлов в директории: {sql_files_directory}")
                return

            for file_path in view_files:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        sql_script = file.read()
                        self.cursor.execute(sql_script)
                        self.conn.commit()
                        logging.info(f"Database: Выполнено: {file_path}")
                except Exception as e:
                    logging.error(f"Database: Ошибка в {file_path}: {e}")
                    self.conn.rollback()
        finally:
            self._close()
