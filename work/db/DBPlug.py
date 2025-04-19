from abc import ABC, abstractmethod
from typing import List

from interfaces.ISimpleDB import IDatabase

from model.Entry import Entry as IEntry
# needs to be replaced with this!! somehow
# from interfaces.IEntry import IEntry


class DBPlug(IDatabase):

	def __init__(self):
		self.data = []  # best database

	def initialize(self, config):
		print("Initializing db from config, blahblah")

	def init_tables(self):
		print("Init tables wohoo")

	def put_into_db(self, entries: List[IEntry]):
		print(f"Extending by {entries}")
		self.data.extend(entries)

	def get_all_entries(self) -> List[IEntry]:
		print(f"Return {self.data}")
		return self.data

	def query(self, query_text):
		print("Ye, right, no query for you from dbplug")
		return "Eat pipes"
