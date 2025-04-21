from typing import List, Tuple, Any

from interfaces.IApp import IApp, IController
from interfaces.IView import IView
from model.Entry import Entry as IEntry

# A bit lying with name there, supposed to be ViewApp
class CLIApp(IApp):


    def __init__(self, controller: IController, view: IView):
        self.controller = controller
        self.view = view
        self.running = True
        self.commands_dict = {
            "parse": (lambda *args: self.controller.parse(*args)),
            "get_cache": (lambda *args: self.view.handle_show_cache(self.controller.get_cache())),
            "post": (lambda *args: self.controller.post()),
            "get_views": (lambda *args: self.handle_get_views()),
            "get_view_data": (lambda *args:
                self.view.handle_getall(  # one needs to put dict there
                    [IEntry(*e) for e in
                     self.controller.get_view_data(args[0]).itertuples(index=False, name=None)]
                )
            ),
            # "get_requests_by_ip_and_date": (lambda *args:
            #     self.view.handle_getall(  # one needs to put dict there
            #         [IEntry(*e) for e in
            #         self.controller.get_requests_by_ip_and_date().itertuples(index=False, name=None)]
            #     )
            # ),
            "create_tables": (lambda *args: self.controller.create_tables(*args)),
            "create_views": (lambda *args: self.controller.create_views(*args)),
            "stop": (lambda *args: self.stop()),
            "help": (lambda *args: self.help(*args))
        }
        self.commands_descriptions = {
            "parse": "parse",
            "get_cache": "get_cache",
            "post": "post",
            "get_views": "get_views",
            "get_view_data": "get_view_data",
            # "get_requests_by_ip_and_date": "get_requests",
            "create_tables": "create_tables",
            "create_views": "create_views",
            "stop": "Stops the program. No arguments",
            "help": "Helps you by describing commands. " +
                    "If no argument - lists all available commands, " +
                    "if one argument - tells about a specified command"
        }


    def run(self):
        self.view.msg("Welcome to CLI interface, enter 'help' for awailable commands")
        while self.running:
            command, args = self.view.input()
            self.do_command(command, args)

    def do_command(self, command, args):
        if command in self.commands_dict:
            (self.commands_dict[command])(*args)
        else:
            self.view.error_msg(f"No known command {command}")

    def handle_get_views(self):
        for view in self.controller.get_views():
            self.view.msg(view)

    def stop(self):
        self.running = False

    def help(self, command=None):
        if command is None:
            self.view.msg("Available commands: ")
            for key in self.commands_dict.keys():
                self.view.msg(key)
            return
        if command in self.commands_dict.keys():
            self.view.msg(self.commands_descriptions[command])
            return
        self.view.msg(f"No known command {command}")