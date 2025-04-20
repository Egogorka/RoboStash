from abc import ABC, abstractmethod

from interfaces.IController import IController


class IApp(ABC):
    """
    Examples of this class are "GUIApp", and "CLIApp"
    previously the logic was Parser -> DB -> Visualizer, while App handled commands.
    But because Qt handles the app cycle within itself and is Event based,
    I kinda split logic into (Parser + DB + App_old(without cycle)) -> Controller,
    and Visualizer + Run_cycle -> App
    """

    @abstractmethod
    def __init__(self, controller: IController, *args):
        """
        Sets up controller as a parameter of self, and uses it's commands
        :param controller:
        :param args:
        """
        pass

    @abstractmethod
    def run(self):
        """
        Run the controller
        :return:
        """
        pass