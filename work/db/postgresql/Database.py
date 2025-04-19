from interfaces.IDatabase import IDatabase
from parser.PostgresLoader import PostgresLoader
from parser.Parser import Parser
import psycopg2
import glob 
import pandas as pd

class Database(IDatabase):
    def __init__(self, connection_params):
        self.connection_params = connection_params

    def _connect(self):
        self.conn = psycopg2.connect(**self.connection_params)
        self.cursor = self.conn.cursor()

    def _close(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    def create_tables(self, sql_files_directory='./sql_scripts/table'):
        self.execute_sql_files_directory(sql_files_directory)
        print("Таблицы созданы")
    
    def create_views(self, sql_files_directory='./sql_scripts/views'):
        self.execute_sql_files_directory(sql_files_directory)
        print("Представления созданы")

    def load_log(self, log_path: str):
        if not hasattr(self, 'loader'):
            self.loader = PostgresLoader(self.connection_params)
        p=Parser()
        self.loader.load_log(p.parse(log_path))

    def get_view_data(self, view_name: str) -> pd.DataFrame:
        with self._connect_function() as conn:
            return pd.read_sql_query(f"SELECT * FROM {view_name}", conn)

    def get_requests_by_ip_and_date(self):
        df = self.get_view_data("view_requests_by_ip_and_date")
        pivot_df = df.pivot_table(index='ip_address', columns='date', values='count', fill_value=0)
        return pivot_df

    def execute_sql_files_directory(self, sql_files_directory):
        self._connect()
        try:
            view_files = glob.glob(f"{sql_files_directory}/*.sql")
            if not view_files:
                print(f"No SQL files found in directory: {sql_files_directory}")
                return

            for file_path in view_files:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        sql_script = file.read()
                        self.cursor.execute(sql_script)
                        self.conn.commit()
                        print(f"Executed: {file_path}")
                except Exception as e:
                    print(f"Error in {file_path}: {e}")
                    self.conn.rollback()
        finally:
            self._close()

