import yaml
try:
	from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
	from yaml import Loader, Dumper

from applications.cli.CLIApp import CLIApp
from applications.cli.CLIView import CLIView

from applications.gui.QTApp import QTApp

from controller.Controller import Controller

from db.DBPlug import DBPlug
from db.postgresql.Database import Database as PostgreSQL_DB

from parser.ParserPlug import ParserPlug
from parser.Parser import Parser

import sys

class MainManager():
	controller = None
	app = None

	def __init__(self):
		with open('example_config.yaml', 'r') as f:
			settings = yaml.load(f, Loader=Loader)
			print(settings)
			selected_db = settings["settings"]["database"]

			# set parser
			if settings["settings"]["parser"] == "default":
				print("Default parser is used")
				parser = Parser()
			else:
				if settings["settings"]["parser"] != "plug":
					print("Name for parser not found, plug is used")
				else:
					print("Plug is used for parser")
				parser = ParserPlug()

			# set database
			db = None
			if selected_db not in settings["databases"]:
				print("Name for database not found, plug is used")
				selected_db = "plug"

			if selected_db == "plug":
				db = DBPlug(settings["databases"][selected_db])
			if selected_db == "postgreSQL":
				db = PostgreSQL_DB(settings["databases"][selected_db])

			# create controller
			self.controller = Controller(parser=parser, db=db)

			# set app
			if settings["settings"]["view"] == "cli":
				self.app = CLIApp(self.controller, CLIView())
			if settings["settings"]["view"] == "gui":
				self.app = QTApp(self.controller, sys.argv)


if __name__ == "__main__":
	Manager = MainManager()
	Manager.app.run()
