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
from os.path import isfile, join, dirname, splitext
from os import listdir

import logging
from Logging.Logging_configuration.logging_basic_config import set_basic_config


class MainManager():
	controller = None
	app = None

	def __init__(self, python_args: list[str]):
		set_basic_config()

		cur_dir = dirname(python_args[0])
		config_files = [f for f in listdir(cur_dir)
			if isfile(join(cur_dir, f)) and splitext(f)[1] == ".yaml"
		]
		config_path = "example_config.yaml"
		if "config.yaml" in config_files:
			config_path = "config.yaml"
		elif "example_config.yaml" not in config_files:
			logging.info("Neither 'config.yaml' nor 'example_config.yaml' is present. Abort")
			return
		else:
			logging.info("No 'config.yaml' in current directory, using 'example_config.yaml'")

		with open(config_path, 'r') as f:
			settings = yaml.load(f, Loader=Loader)
			selected_db = settings["settings"]["database"]

			# set parser
			if settings["settings"]["parser"] == "default":
				logging.info("Default parser is used")
				parser = Parser()
			else:
				if settings["settings"]["parser"] != "plug":
					logging.info("Name for parser not found, plug is used")
				else:
					logging.info("Plug is used for parser")
				parser = ParserPlug()

			# set database
			db = None
			if selected_db not in settings["databases"]:
				selected_db = "plug"

			if selected_db == "plug":
				db = DBPlug(settings["databases"][selected_db])
				logging.info("Name for database not found, plug is used")
			if selected_db == "postgreSQL":
				db = PostgreSQL_DB(settings["databases"][selected_db])

			# create controller
			self.controller = Controller(parser=parser, db=db)

			# set app
			if settings["settings"]["view"] == "cli":
				self.app = CLIApp(self.controller, CLIView())
			if settings["settings"]["view"] == "gui":
				self.app = QTApp(self.controller, python_args)


if __name__ == "__main__":
	Manager = MainManager(sys.argv)
	Manager.app.run()
