import yaml
try:
	from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
	from yaml import Loader, Dumper

from applications.cli.CLIApp import CLIApp
from applications.cli.CLIView import CLIView

from controller.Controller import Controller
from db.DBPlug import DBPlug
from parser.ParserPlug import ParserPlug

if __name__ == "__main__":
	app = None
	parser = ParserPlug()
	db = None
	controller = None
	with open('example_config.yaml', 'r') as f:
		settings = yaml.load(f, Loader=Loader)
		print(settings)

		# set parser

		# set database
		if settings["database"]["type"] == "plug":
			db = DBPlug()
		db.initialize(settings["database"])

		controller = Controller(parser=parser, db=db)

		# set app
		if settings["settings"]["view"] == "cli":
			app = CLIApp(controller, CLIView())
	app.run()
