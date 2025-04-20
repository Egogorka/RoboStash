from PySide6.QtWidgets import QFileDialog

import tkinter as tk
from tkinter import filedialog


class LogAnalyzerController():

    def __init__(self, gui, controller):
        self.gui = gui
        self.controller = controller

    def get_file_path():
        root = tk.Tk()
        root.withdraw()
        
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=((".log", ".log"),)
        )
        return file_path if file_path else None

    def get_date_value_pairs():
        date_value_pairs = [
        ("2025-01-01", 150),
        ("2025-01-02", 230),
        ("2025-01-03", 180),
        ("2025-01-04", 210)
        ]
        return date_value_pairs
    
    def get_ip_data():
        ip_data = {
            "192.168.1.1": 45,
            "192.168.1.2": 32,
            "192.168.1.3": 28,
            "192.168.1.4": 22,
            "192.168.1.5": 20,
            "192.168.1.6": 15,
            "192.168.1.7": 8,
            "192.168.1.8": 3,
        }
        return ip_data
    
    def get_request_data():
        sample_data = [
            {
                "ip": "192.168.1.1",
                "protocol": "HTTP/1.1",
                "device": "Desktop",
                "browser": "Chrome",
                "version": "116.0.5845.141",
                "total": 148
            },
            {
                "ip": "192.168.1.2",
                "protocol": "HTTP/2",
                "device": "Mobile",
                "browser": "Safari",
                "version": "16.6",
                "total": 92
            }
        ]
        return sample_data
    
    def db_load_result(self, result_string):
        self.gui.status_bar.showMessage(result_string, 3000)

    def get_error_data():
        error_data = [
            ("2023-01-01", 12),
            ("2023-01-02", 25),
            ("2023-01-03", 18),
            ("2023-01-04", 15),
            ("2023-01-05", 22)
        ]
        return error_data
    
    def get_error_types():
        error_types = {
            "Client Errors": {
                "400 Bad Request": 15,
                "401 Unauthorized": 8,
                "403 Forbidden": 10,
                "404 Not Found": 65
            },
            "Server Errors": {
                "500 Internal Error": 25,
                "502 Bad Gateway": 7,
                "503 Service Unavailable": 5,
                "504 Gateway Timeout": 3,
                "404 Zrada": 3
            }
        }
        return error_types
        
        
