from abc import ABC, abstractmethod
from typing import List

from interfaces.IDatabase import IDatabase

from model.Entry import Entry as IEntry
# needs to be replaced with this!! somehow
# from interfaces.IEntry import IEntry

import pandas as pd

class DBPlug(IDatabase):

	def __init__(self, config):
		print("Initializing db from config:")
		print(config)
		self.data = []  # best database

	def _connect(self):
		print("Connect to database")

	def _close(self):
		print("Close database connection")

	def create_tables(self, sql_files_directory=None):
		print(f"PLUG: Create tables with {sql_files_directory}")

	def create_views(self, sql_files_directory=None):
		print(f"PLUG: Create views with {sql_files_directory}")

	def load_log(self, entries: List[IEntry]):
		self.data.extend(entries)

	def get_view_data(self, view_name: str) -> pd.DataFrame:
		return pd.DataFrame()

	def get_views(self) -> List[str]:
		return []  # no views

	def get_requests_by_ip_and_date(self) -> pd.DataFrame:
		return pd.DataFrame.from_records([e.to_dict() for e in self.data])