from interfaces.ISimpleDB import IDatabase
from interfaces.IParser import IParser


class CacheEntry:

	def __init__(self, command, details, data):
		self.command = command
		self.details = details
		self.data = data


class App:
	# Stupid Python does not allow the usage
	# of class inside of itself.
	commands_dict = {}

	def __init__(self, db: IDatabase, parser: IParser, view):
		self.db = db
		self.parser = parser
		self.view = view

		self.cache = []
		self.running = True

	def run(self):
		while self.running:
			command, args = self.view.input()
			if command in self.commands_dict:

				self.commands_dict[command](self, *args)

			else:
				self.view.error_msg(f"No known command {command}")

	def parse(self, path):
		data = self.parser.parse(path)
		self.cache.append(
			CacheEntry("parse", path, data)
		)

	def post(self):
		for cache_entry in self.cache:
			self.db.put_into_db(cache_entry.data)
		self.cache = []  # empty the cache

	def get_all(self):
		response = self.db.get_all_entries()
		self.view.handle_getall(response)

	def get(self, query):
		response = self.db.query(query)
		self.view.handle_query(query, response)

	def stop(self):
		self.running = False


App.commands_dict = {
		"parse": App.parse,
		"post": App.post,
		"get_all": App.get_all,
		"get": App.get,
		"quit": App.stop
}
