from PySide6.QtWidgets import QFileDialog

import tkinter as tk
import os
from tkinter import filedialog


class LogAnalyzerController():

    def __init__(self, gui, controller, db):
        self.gui = gui
        self.controller = controller
        self.db = db

    def get_file_path():
        root = tk.Tk()
        root.withdraw()
        
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=((".log", ".log"),)
        )
        return file_path if file_path else None

    def get_date_value_pairs(self):
        df = self.db.get_view_data("view_count_requests_by_day", 10)
        dict = df.to_dict(orient='records')
        date_value_pairs = [(item["date"], item["total_requests"]) for item in dict]
        return date_value_pairs
    
    def get_ip_data(self):
        df = self.db.get_view_data("view_count_requests_by_day", 10)
        dict = df.to_dict(orient='records')
        ip_data = {item["ip_address"]: item["total_requests"] for item in dict}
        return ip_data
    
    def get_request_data(self):
        df = self.db.get_view_data("view_count_ip_requests", 10)
        sample_data = df.to_dict(orient='records')
        return sample_data
    
    def db_load_result(self, result_string):
        self.gui.status_bar.showMessage(result_string, 3000)

    def get_error_data(self):
        df = self.db.get_view_data("view_count_failed_requests_by_day", 10)
        dict = df.to_dict(orient='records')
        error_data = [(item["date"], item["total_failed"]) for item in dict]
        return error_data
    
    def get_error_types(self):
        df = self.db.get_view_data("view_count_status_code")
        dict = df.to_dict(orient='records')
        error_data = {item["status_code"]: item["total"] for item in dict}
        return error_data
    
    def save_to_csv(self, output_directory: str = './csv_files'):
        for view_name in ["view_requests_by_ip_day", "view_count_requests_by_day", "view_top_ips", 
                      "view_count_ip_requests", "view_count_failed_requests_by_day", "view_count_status_code", 
                      "view_fact_logs"]:
            print(f"Получаем данные для представления: {view_name}")
            
            df = self.db.get_view_data(view_name)

            field_names = df.columns.tolist()
            print(f"Названия полей для {view_name}: {', '.join(map(str, field_names))}")

            csv_filename = os.path.join(output_directory, f"{view_name}.csv")

            self.db.save_dict_to_csv(df.to_dict(orient='records'), csv_filename)
            print(f"Данные для представления {view_name} сохранены в файл {csv_filename}")
        
        
