from PySide6.QtWidgets import QFileDialog

class LogAnalyzerController:

    def __init__(self, gui):
        self.gui = gui
        self._connect_actions()
        
    def _connect_actions(self):
        self.gui.browse_btn.clicked.connect(self._browse_files)
        self.gui.load_btn.clicked.connect(self._load_data)
        self.gui.export_btn.clicked.connect(self._export_data)

    def _browse_files(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.gui, 
            "Select Log File", 
            "", 
            "Log Files (*.log);;All Files (*)"
        )
        if file_path:
            self.gui.file_path_edit.setText(file_path)
            self.gui.status_bar.showMessage("File selected", 3000)

    def _load_data(self):
        self.gui.status_bar.showMessage("Data loaded successfully", 3000)

    def _export_data(self):
        format = self.gui.format_combo.currentText()
        self.gui.status_bar.showMessage(f"Exporting to {format}...", 3000)