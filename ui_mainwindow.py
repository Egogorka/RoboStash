from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QTabWidget,
    QComboBox,
    QStatusBar,
    QTableView,
    QGroupBox,
    QSplitter,
    QHeaderView,
)
from PySide6.QtCore import Qt
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QBarSeries,
    QBarSet,
    QValueAxis,
    QCategoryAxis,
    QLineSeries,
    QPieSeries,
    QLegend,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPainter, QColor

from logic_gui import LogAnalyzerController

from applications.cli.CLIApp import CLIApp
from applications.cli.CLIView import CLIView
from applications.gui.QTApp import QTApp
from controller.Controller import Controller
from db.DBPlug import DBPlug
from parser.ParserPlug import ParserPlug

class LogAnalyzerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Log Analysis Tool')
        self.setGeometry(100, 100, 1000, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        load_group = QGroupBox("Data Loading")
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)
        self.browse_btn = QPushButton("Select Log File")
        self.load_btn = QPushButton("Load to Database")

        load_layout = QHBoxLayout()
        load_layout.addWidget(self.file_path_edit)
        load_layout.addWidget(self.browse_btn)
        load_layout.addWidget(self.load_btn)
        load_group.setLayout(load_layout)

        status_group = QGroupBox("Export Status")
        self.status_bar = QStatusBar()
        status_layout = QHBoxLayout()
        status_layout.addWidget(self.status_bar)
        status_group.setLayout(status_layout)

        export_group = QGroupBox("Data Export")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["CSV", "Parquet"])
        self.export_btn = QPushButton("Export Data")

        export_layout = QHBoxLayout()
        export_layout.addWidget(QLabel("Export Format:"))
        export_layout.addWidget(self.format_combo)
        export_layout.addWidget(self.export_btn)
        export_group.setLayout(export_layout)

        self.tabs = QTabWidget()
        self._init_tabs()
        self._connect_actions()

        main_layout.addWidget(load_group)
        main_layout.addWidget(status_group)
        main_layout.addWidget(export_group)
        main_layout.addWidget(self.tabs)

    def _connect_actions(self):
        self.browse_btn.clicked.connect(self.handle_browse) 
        self.load_btn.clicked.connect(self.load_log_file)     
        self.export_btn.clicked.connect(self.export_db)

    def export_db(self):
        format = self.format_combo.currentData()
        if format == "csv":
            LogAnalyzerController.save_to_csv()
        elif format == "Parquet":
            pass

    def handle_browse(self):
        file_path = LogAnalyzerController.get_file_path()
        if file_path:
            self.file_path_edit.setText(file_path)
            self.status_bar.showMessage(f"Selected file: {file_path}", 3000)

    def load_log_file(self):

        file_path = self.file_path_edit.text()
        
        if not file_path:
            self.status_bar.showMessage("Error: No file selected", 3000)
            return False
        Controller.parse(Controller, file_path)
        self._init_tabs()

    def _init_tabs(self):
        self.tabs = QTabWidget()
        
        self.requests_tab = QWidget()
        self.ip_table_tab = QWidget()
        self.errors_tab = QWidget()
        
        self._init_requests_tab()
        self._init_ip_table_tab()
        self._init_errors_tab()
        
        self.tabs.addTab(self.requests_tab, "Request Statistics")
        self.tabs.addTab(self.ip_table_tab, "IP/Daily Activity")
        self.tabs.addTab(self.errors_tab, "Error Analysis")


    def _init_requests_tab(self):
        splitter = QSplitter()
        
        line_chart = QChart()
        line_chart.setTitle("Requests by Date")
        line_series = QLineSeries()

        date_value_pairs = LogAnalyzerController.get_date_value_pairs(LogAnalyzerController)

        for i, (date, value) in enumerate(date_value_pairs):
            line_series.append(i, value)

            axis_x = QCategoryAxis()
            axis_x.setTitleText("Date")
            axis_x.append(date, i) 

        line_chart.addSeries(line_series)
        line_chart.addAxis(axis_x, Qt.AlignBottom)
        line_series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setTitleText("Number of Requests")
        line_chart.addAxis(axis_y, Qt.AlignLeft)
        line_series.attachAxis(axis_y)
        
        line_chart_view = QChartView(line_chart)
        line_chart_view.setRenderHint(QPainter.Antialiasing)
        
        bar_chart = QChart()
        bar_chart.setTitle("Top IPs by Requests")
        bar_series = QBarSeries()

        ip_data = LogAnalyzerController.get_ip_data(LogAnalyzerController)
        
        bar_set = QBarSet("Requests")
        for count in ip_data.values():
            bar_set.append(count)
        bar_series.append(bar_set)
        bar_chart.addSeries(bar_series)
        
        axis_x_bar = QCategoryAxis()
        axis_x_bar.setTitleText("IP Address")
        for i, ip in enumerate(ip_data.keys()):
            axis_x_bar.append(f"{ip}", i + 0.5)
            bar_chart.addAxis(axis_x_bar, Qt.AlignBottom)
            bar_series.attachAxis(axis_x_bar)
        
        axis_y_bar = QValueAxis()
        axis_y_bar.setTitleText("Count")
        bar_chart.addAxis(axis_y_bar, Qt.AlignLeft)
        bar_series.attachAxis(axis_y_bar)
        
        bar_chart_view = QChartView(bar_chart)
        bar_chart_view.setRenderHint(QPainter.Antialiasing)
        
        splitter.addWidget(line_chart_view)
        splitter.addWidget(bar_chart_view)
        
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        self.requests_tab.setLayout(layout)

    def _init_ip_table_tab(self):
        layout = QVBoxLayout()
        
        self.ip_table = QTableView()
        model = QStandardItemModel()
        
        headers = [
            "IP Address",
            "Protocol Version",
            "Device Type",
            "Browser",
            "Browser Version",
            "Total Requests"
        ]
        model.setHorizontalHeaderLabels(headers)
        
        sample_data = LogAnalyzerController.get_request_data(LogAnalyzerController)

        for data in sample_data:
            row = [
                QStandardItem(data["ip"]),
                QStandardItem(data["protocol"]),
                QStandardItem(data["device_type"]),
                QStandardItem(data["os_family"]),
                QStandardItem(data["os_version"]),
                QStandardItem(data["browser_family"]),
                QStandardItem(data["browser_version"]),
                QStandardItem(data["device_brand"]),
                QStandardItem(data["device_model"]),
                QStandardItem(str(data["total"]))
            ]
            model.appendRow(row)
        
        self.ip_table.setModel(model)
        self.ip_table.setAlternatingRowColors(True)
        self.ip_table.setSelectionBehavior(QTableView.SelectRows)
        self.ip_table.setSelectionMode(QTableView.SingleSelection)
        self.ip_table.setSortingEnabled(True)
        
        header = self.ip_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # IP
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Protocol
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Device Type
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # OS Family
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # OS Version
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Browser Family
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Browser Version
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # Device Brand
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)  # Device Model
        header.setSectionResizeMode(9, QHeaderView.ResizeToContents)  # Total Requests
        
        layout.addWidget(self.ip_table)
        self.ip_table_tab.setLayout(layout)

    def _init_errors_tab(self):
        splitter = QSplitter(Qt.Horizontal)
        
        line_chart = QChart()
        line_chart.setTitle("Error Trends")
        line_series = QLineSeries()

        error_data = LogAnalyzerController.get_error_data(LogAnalyzerController)
        for i, (date, count) in enumerate(error_data):
            line_series.append(i, count)
            line_series.setName(f"{date}: {count} errors")
        
        line_chart.addSeries(line_series)
        
        axis_x = QCategoryAxis()
        axis_x.setTitleText("Date")
        for i, (date, _) in enumerate(error_data):
            axis_x.append(date, i)
        line_chart.addAxis(axis_x, Qt.AlignBottom)
        line_series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        axis_y.setTitleText("Error Count")
        line_chart.addAxis(axis_y, Qt.AlignLeft)
        line_series.attachAxis(axis_y)
        
        line_chart_view = QChartView(line_chart)
        line_chart_view.setRenderHint(QPainter.Antialiasing)
        
        pie_chart = QChart()
        pie_chart.setTitle("Error")
        pie_chart.setAnimationOptions(QChart.SeriesAnimations)
        pie_chart.legend().setVisible(True)
        pie_chart.legend().setAlignment(Qt.AlignRight)
        pie_chart.legend().setMarkerShape(QLegend.MarkerShapeCircle)

        error_types = LogAnalyzerController.get_error_types(LogAnalyzerController)

        colors = [
            "#e74c3c", "#c0392b", "#e67e22", "#d35400", 
            "#3498db", "#2980b9", "#1abc9c", "#16a085"  
        ]
        pie_series = QPieSeries()
        color_index = 0

        for i, record in enumerate(error_types):
            status_code = record['status_code']
            count = record['total']
            name = f"{status_code} {self._get_status_name(status_code)}"
    
            slice = pie_series.append(f"{name} ({count})", count)
            slice.setColor(QColor(colors[color_index % len(colors)]))
            slice.setLabelVisible(True)
            slice.setLabelArmLengthFactor(0.2)
            color_index += 1
        
        pie_series.setLabelsVisible(True)

        for slice in pie_series.slices():
            slice.hovered.connect(lambda state, s=slice: 
                                s.setExploded(state) or s.setLabelVisible(state))
        
        pie_chart.addSeries(pie_series)
        pie_container = QWidget()
        pie_layout = QVBoxLayout()
        pie_chart_view = QChartView(pie_chart)
        pie_chart_view.setRenderHint(QPainter.Antialiasing)
        pie_layout.addWidget(pie_chart_view)
        
        total_errors = sum(sum(errors.values()) for errors in error_types.values())
        stats_label = QLabel(
            f"<b>Error Summary:</b><br>"
            f"Total Errors: {total_errors}<br>"
            f"Client Errors (4xx): {sum(error_types['Client Errors'].values())} "
            f"({sum(error_types['Client Errors'].values())/total_errors*100:.1f}%)<br>"
            f"Server Errors (5xx): {sum(error_types['Server Errors'].values())} "
            f"({sum(error_types['Server Errors'].values())/total_errors*100:.1f}%)"
        )
        stats_label.setAlignment(Qt.AlignLeft)
        pie_layout.addWidget(stats_label)
        
        pie_container.setLayout(pie_layout)
        
        splitter.addWidget(line_chart_view)
        splitter.addWidget(pie_container)
        
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        self.errors_tab.setLayout(layout)