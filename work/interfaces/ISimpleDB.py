from abc import ABC, abstractmethod
from typing import List
from interfaces.IEntry import IEntry
from model.Entry import Entry as IEntry
# needs to be replaced with this!! somehow
# from interfaces.IEntry import IEntry


class IDatabase(ABC):
	@abstractmethod
	def initialize(self, config):
		pass  # create connection with DB there

	@abstractmethod
	def init_tables(self):
		pass

	@abstractmethod
	def put_into_db(self, entries: List[IEntry]):
		pass

	@abstractmethod
	def get_all_entries(self) -> List[IEntry]:
		pass

	@abstractmethod
	def query(self, query_text):
		pass
