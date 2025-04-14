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
from parser.ParserPlug import ParserPlug

import sys

if __name__ == "__main__":
	app = None
	with open('example_config.yaml', 'r') as f:
		settings = yaml.load(f, Loader=Loader)
		print(settings)

		# set parser
		parser = ParserPlug()

		# set database
		db = None
		if settings["database"]["type"] == "plug":
			db = DBPlug()
		db.initialize(settings["database"])

		# create controller
		controller = Controller(parser=parser, db=db)

		# set app
		if settings["settings"]["view"] == "cli":
			app = CLIApp(controller, CLIView())
		if settings["settings"]["view"] == "gui":
			app = QTApp(controller, sys.argv)
	app.run()
