from typing import List, Tuple, Any

from interfaces.IApp import IApp, IController
from interfaces.IView import IView


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
            "get_all": (lambda *args: self.view.handle_getall(self.controller.get_all())),
            "query": (lambda query: self.view.handle_query(query, self.controller.query(query))),
            "stop": (lambda *args: self.stop()),
            "help": (lambda *args: self.help(*args))
        }
        self.commands_descriptions = {
            "parse": "parse",
            "get_cache": "get_cache",
            "post": "post",
            "get_all": "get_all",
            "query": "Executes the ",
            "stop": "Stops the program. No arguments",
            "help": "Helps you by describing commands. " +
                    "If no argument - lists all available commands, " +
                    "if one argument - tells about a specified command"
        }


    def run(self):
        while self.running:
            command, args = self.view.input()
            self.do_command(command, args)

    def do_command(self, command, args):
        if command in self.commands_dict:
            self.commands_dict[command](*args)
        else:
            self.view.error_msg(f"No known command {command}")

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