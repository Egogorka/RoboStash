import sys
from PySide6.QtWidgets import QApplication
from applications.gui.ui_mainwindow import LogAnalyzerGUI
from applications.gui.logic_gui import LogAnalyzerController

from interfaces.IApp import IApp
from interfaces.IController import IController

class QTApp(IApp):

    def __init__(self, controller: IController, argv):
        self._app = QApplication(argv)
        self._view = LogAnalyzerGUI()
        LogAnalyzerController(self._view, controller)  # connect handlers

    def run(self):
        self._view.show()
        sys.exit(self._app.exec_())
