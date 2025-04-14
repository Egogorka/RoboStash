from interfaces.ISimpleDB import IDatabase
from interfaces.IParser import IParser
from interfaces.IController import IController
from model.Entry import Entry as IEntry

from typing import List

import itertools

class CacheEntry:

	def __init__(self, command, details, data):
		self.command = command
		self.details = details
		self.data = data


class Controller(IController):

	def __init__(self, db: IDatabase, parser: IParser):
		self.db = db
		self.parser = parser

		self.cache = []

	def parse(self, path):
		data = self.parser.parse(path)
		self.cache.append(
			CacheEntry("parse", path, data)
		)

	def get_cache(self) -> List[IEntry]:
		temp = [entry.data for entry in self.cache]
		return list(itertools.chain.from_iterable(temp))

	def post(self):
		for cache_entry in self.cache:
			self.db.put_into_db(cache_entry.data)
		self.cache = []  # empty the cache

	def get_all(self):
		return self.db.get_all_entries()

	def query(self, query):
		return self.db.query(query)