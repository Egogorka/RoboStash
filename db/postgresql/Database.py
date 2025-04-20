from interfaces.IDatabase import IDatabase
from db.postgresql.PostgresLoader import PostgresLoader
import psycopg2
import glob
import pandas as pd

from model.Entry import Entry as IEntry
from typing import List


class Database(IDatabase):

    def __init__(self, settings):
        self.settings = settings
        self.loader = PostgresLoader(self._connect_function)

    def _connect_function(self):
        dbname = self.settings["dbname"]
        user = self.settings["user"]
        password = self.settings["password"]
        port = self.settings["port"]
        host = self.settings["host"]
        print(self.settings)
        return psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def _connect(self):
        self.conn = self._connect_function()
        self.cursor = self.conn.cursor()

    def _close(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    def create_tables(self, sql_files_directory=None):
        if sql_files_directory is None:
            sql_files_directory = self.settings["scripts"]["table"]
        self.execute_sql_files_directory(sql_files_directory)

    def create_views(self, sql_files_directory=None):
        if sql_files_directory is None:
            sql_files_directory = self.settings["scripts"]["views"]
        self.execute_sql_files_directory(sql_files_directory)

    def load_log(self, entries: List[IEntry]):
        logs = [entry.all for entry in entries]
        parsed_ua = [entry.ua.all for entry in entries]
        self.loader.load_log(logs, parsed_ua)

    def get_views(self) -> List[str]:
        print("NOT IMPLEMENTED!")
        return []

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
                    with open(file_path, 'r') as file:
                        sql_script = file.read()
                        self.cursor.execute(sql_script)
                        self.conn.commit()
                        print(f"Executed: {file_path}")
                except Exception as e:
                    print(f"Error in {file_path}: {e}")
                    self.conn.rollback()
        finally:
            self._close()
