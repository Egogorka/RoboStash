from abc import ABC, abstractmethod
from typing import List

from model.Entry import Entry as IEntry
# needs to be replaced with this!! somehow
# from interfaces.IEntry import IEntry

# big brain file


class IParser(ABC):

	@abstractmethod
	def parse(self, path: str) -> List[IEntry]:
		pass
