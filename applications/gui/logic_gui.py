from PySide6.QtWidgets import QFileDialog

import tkinter as tk
from tkinter import filedialog

class FilePathFinder():

    def get_file_path():
        root = tk.Tk()
        root.withdraw()
        
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=(("Все файлы", "*.*"),)
        )
        return file_path if file_path else None

class LogAnalyzerController():

    def __init__(self, gui, controller):
        self.gui = gui
        self.controller = controller

    def _browse_files(self):
        print("click")
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
        print("click")
        self.gui.status_bar.showMessage("Data loaded successfully", 3000)

    def _export_data(self):
        print("click")
        format = self.gui.format_combo.currentText()
        self.gui.status_bar.showMessage(f"Exporting to {format}...", 3000)