import sys
from PySide6.QtWidgets import QApplication
from ui_mainwindow import LogAnalyzerGUI
from logic_gui import LogAnalyzerController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = LogAnalyzerGUI()
    view.show()
    sys.exit(app.exec_())