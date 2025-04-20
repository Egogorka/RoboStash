from interfaces.IDatabase import IDatabase
from interfaces.IParser import IParser
from interfaces.IController import IController
from model.Entry import Entry as IEntry

import pandas as pd

from typing import List

import itertools

class CacheEntry:

	def __init__(self, command, details, data):
		self.command = command
		self.details = details
		self.data = data


class Controller(IController):

	def __init__(self, db: IDatabase, parser: IParser):
		self._db = db
		self._parser = parser

		self.cache = []

	def parse(self, path):
		try:
			data = self._parser.parse(path)
			self.cache.append(
				CacheEntry("parse", path, data)
			)
		except FileNotFoundError as e:
			print(str(e))

	def get_cache(self) -> List[IEntry]:
		temp = [entry.data for entry in self.cache]
		return list(itertools.chain.from_iterable(temp))

	def post(self):
		for cache_entry in self.cache:
			self._db.load_log(cache_entry.data)
		self.cache = []  # empty the cache

	def get_views(self) -> List[str]:
		return self._db.get_views()

	def get_view_data(self, view_name: str) -> pd.DataFrame:
		return self._db.get_view_data(view_name)

	def get_requests_by_ip_and_date(self):
		return self._db.get_requests_by_ip_and_date()

	def create_tables(self, sql_files_directory=None):
		return self._db.create_tables(sql_files_directory)

	def create_views(self, sql_files_directory=None):
		return self._db.create_views(sql_files_directory)