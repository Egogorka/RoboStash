from interfaces.IDatabase import IDatabase
from parser.PostgresLoader import PostgresLoader
import psycopg2
import glob 
import pandas as pd

class Database(IDatabase):
    def __init__(self, connection_params):
        self.connection_params = connection_params
        self.loader = PostgresLoader(self._connect())

    def _connect(self):
        """Устанавливает подключение к базе данных."""
        self.conn = psycopg2.connect(**self.connection_params)
        self.cursor = self.conn.cursor()

    def _close(self):
        """Закрывает соединение с базой данных."""
        if self.conn:
            self.cursor.close()
            self.conn.close()

    def create_tables(self, sql_files_directory='./sql_scripts/table'):
        """Создает таблицы и индексы"""
        self.execute_sql_files_directory(sql_files_directory)
    
    def create_views(self, sql_files_directory='./sql_scripts/views'):
        """Создает представления"""
        self.execute_sql_files_directory(sql_files_directory)

    def load_log(self, log_path: str):
        self.loader.load_log(log_path)
    
    def get_view_data(self, view_name: str) -> pd.DataFrame:
        """
        Возвращает данные из указанного представления в виде pandas DataFrame.
        
        :param view_name: Название представления в базе данных.
        :return: DataFrame с данными из представления.
        """
        self._connect()
        df = pd.read_sql_query(f"SELECT * FROM {view_name}", self.conn)
        self._close()
        return df

    def get_requests_by_ip_and_date(self): #пункт 6
        # Подключение к БД
        conn = self.conn

        # Чтение данных из представления
        df = self.get_view_data("view_requests_by_ip_and_date");

        # Создание сводной таблицы
        pivot_df = df.pivot_table(index='ip_address', columns='date', values='count', fill_value=0)

        conn.close()
        return pivot_df

    def execute_sql_files_directory(self, sql_files_directory):
        """Читает SQL-файлы из указанной директории и выполняет их."""
        self._connect()
        try:
            # Используем glob для поиска всех .sql файлов в директории
            view_files = glob.glob(f"{sql_files_directory}/*.sql")

            if not view_files:
                print(f"No SQL files found in directory: {sql_files_directory}")
                return

            for file_path in view_files:
                try:
                    with open(file_path, 'r') as file:
                        sql_script = file.read()
                        self.cursor.execute(sql_script)
                        self.conn.commit()
                        print(f"View from {file_path} created or replaced successfully.")
                except Exception as e:
                    print(f"Error executing script from {file_path}: {e}")
                    self.conn.rollback()
        finally:
            self._close()
    

    
    
    


# Пример использования
connection_params = {
    'dbname': 'your_db',
    'user': 'your_user',
    'password': 'your_password',
    'host': 'your_host',
    'port': 'your_port'
}

db = IDatabase(connection_params)

# Вызов метода для создания/замены представлений из файлов (с использованием директории по умолчанию)
db.create_views()

