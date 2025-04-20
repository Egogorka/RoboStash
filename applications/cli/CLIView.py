from interfaces.IView import IView, IEntry

from typing import List, Tuple, Any
import re


def quoted_split(s):
	def strip_quotes(s):
		if s and (s[0] == '"' or s[0] == "'") and s[0] == s[-1]:
			return s[1:-1]
		return s
	reg_str = r'(?:[^"\s]*"(?:\\.|[^"])*"[^"\s]*)+|(?:[^\'\s]*\'(?:\\.|[^\'])*\'[^\'\s]*)+|[^\s]+'
	return [strip_quotes(p).replace('\\"', '"').replace("\\'", "'") for p in re.findall(reg_str, s)]


class CLIView(IView):

	def input(self) -> Tuple[str, List[Any]]:
		raw = input("> ")
		raw_split = quoted_split(raw)
		return raw_split[0], raw_split[1:]

	def error_msg(self, s: str):
		print("Error: "+s)

	def msg(self, s: str):
		print(s)

	def handle_show_cache(self, response: List[IEntry]):
		print(f"Amount of entries in cache: {len(response)}")
		for entry in response:
			print(entry)

	def handle_getall(self, response: List[IEntry]):
		for entry in response:
			print(entry)

	def handle_query(self, query: str, response):
		print(f'Query: {query}')
		print(response)  # or whatever
