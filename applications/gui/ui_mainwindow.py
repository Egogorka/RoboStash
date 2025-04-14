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
from logic_gui import FilePathFinder


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
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        main_layout.addWidget(load_group)
        main_layout.addWidget(export_group)
        main_layout.addWidget(self.tabs)

    def _connect_actions(self):
        self.browse_btn.clicked.connect(self.handle_browse) 
        self.load_btn.clicked.connect(self.load_log_file)     
        self.export_btn.clicked.connect(self.dummy_func)   #add btn func

    def dummy_func(self):
        print("click")

    def handle_browse(self):
        file_path = FilePathFinder.get_file_path()
        if file_path:
            self.file_path_edit.setText(file_path)
            self.status_bar.showMessage(f"Selected file: {file_path}", 3000)

    def load_log_file(self):

        file_path = self.file_path_edit.text()
        
        if not file_path:
            self.status_bar.showMessage("Error: No file selected", 3000)
            return False
        print(file_path)
        ## send file_path to log parser

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

        #add func get requests
        dates = ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04"]
        values = [150, 230, 180, 210]
        ###
        for i, (date, value) in enumerate(zip(dates, values)):
            line_series.append(i, value)
        
        line_chart.addSeries(line_series)
        
        axis_x = QCategoryAxis()
        axis_x.setTitleText("Date")
        for i, date in enumerate(dates):
            axis_x.append(date, i)
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
        #add func get top ip
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
        ###
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
        
        #Add func load data request
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
        ##
        for data in sample_data:
            row = [
                QStandardItem(data["ip"]),
                QStandardItem(data["protocol"]),
                QStandardItem(data["device"]),
                QStandardItem(data["browser"]),
                QStandardItem(data["version"]),
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
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Device
        header.setSectionResizeMode(3, QHeaderView.Stretch)          # Browser
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents) # Version
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents) # Total
        
        layout.addWidget(self.ip_table)
        self.ip_table_tab.setLayout(layout)

    def _init_errors_tab(self):
        splitter = QSplitter(Qt.Horizontal)
        
        line_chart = QChart()
        line_chart.setTitle("Error Trends")
        line_series = QLineSeries()
        #add get error data
        error_data = [
            ("2023-01-01", 12),
            ("2023-01-02", 25),
            ("2023-01-03", 18),
            ("2023-01-04", 15),
            ("2023-01-05", 22)
        ]
        ###
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
        #add get error data
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
        ###
        colors = [
            "#e74c3c", "#c0392b", "#e67e22", "#d35400", 
            "#3498db", "#2980b9", "#1abc9c", "#16a085"  
        ]
        pie_series = QPieSeries()
        color_index = 0

        for category, errors in error_types.items():
            for error_code, count in errors.items():
                slice = pie_series.append(f"{error_code} ({count})", count)
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