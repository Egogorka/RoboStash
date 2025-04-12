from abc import ABC, abstractmethod
from typing import List, Tuple, Any

from model.Entry import Entry as IEntry
# needs to be replaced with this!! somehow
# from interfaces.IEntry import IEntry

class IView(ABC):

	"""
	Analogue of native input() Python function, but
	also provides name of the command and list of its arguments
	"""
	@abstractmethod
	def input(self) -> Tuple[str, List[Any]]:
		pass

	@abstractmethod
	def error_msg(self, s: str):
		pass

	@abstractmethod
	def handle_getall(self, response: List[IEntry]):
		pass

	@abstractmethod
	def handle_query(self, query: str, response):
		pass
