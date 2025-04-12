import yaml
try:
	from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
	from yaml import Loader, Dumper

from views.CLIView import CLIView

from application.App import App
from db.DBPlug import DBPlug
from parser.ParserPlug import ParserPlug

if __name__ == "__main__":
	view = None
	parser = None
	db = None
	with open('example_config.yaml', 'r') as f:
		settings = yaml.load(f, Loader=Loader)
		print(settings)

		# set view
		if settings["settings"]["view"] == "cli":
			view = CLIView()

		# set parser
		parser = ParserPlug()

		# set database
		if settings["database"]["type"] == "dbplug":
			db = DBPlug()
		db.initialize(settings["database"])

	app = App(db, parser, view)
	app.run()
