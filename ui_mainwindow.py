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
)
from PySide6.QtCore import Qt
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QBarSeries,
    QBarSet,
    QValueAxis,
    QCategoryAxis,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem


class LogAnalyzerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Log analysis')
        self.setGeometry(100, 100, 1000, 800)

        # Main widgets and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Load section
        load_group = QGroupBox("Download data")
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)
        self.browse_btn = QPushButton("Choose log")
        self.load_btn = QPushButton("Download to DB")

        load_layout = QHBoxLayout()
        load_layout.addWidget(self.file_path_edit)
        load_layout.addWidget(self.browse_btn)
        load_layout.addWidget(self.load_btn)
        load_group.setLayout(load_layout)

        # Export section
        export_group = QGroupBox("Data sender")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["CSV", "Parquet"])
        self.export_btn = QPushButton("Export")

        export_layout = QHBoxLayout()
        export_layout.addWidget(QLabel("Data format:"))
        export_layout.addWidget(self.format_combo)
        export_layout.addWidget(self.export_btn)
        export_group.setLayout(export_layout)

        # Tabs
        self.tabs = QTabWidget()
        self._init_tabs()

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Main layout
        main_layout.addWidget(load_group)
        main_layout.addWidget(export_group)
        main_layout.addWidget(self.tabs)

    def _init_tabs(self):
        self.stats_tab = QWidget()
        self.requests_tab = QWidget()
        self.failures_tab = QWidget()

        self._init_stats_tab()
        self._init_requests_tab()
        self._init_failures_tab()

        self.tabs.addTab(self.stats_tab, "General statistics")
        self.tabs.addTab(self.requests_tab, "Request to IP")
        self.tabs.addTab(self.failures_tab, "Refusal statistics")

    def _init_stats_tab(self):
        layout = QVBoxLayout()
        chart = QChart()
        chart.setTitle("Statistics of request")

        series = QBarSeries()
        bar_set = QBarSet("Requests")
        bar_set.append([100, 200, 150])
        series.append(bar_set)
        chart.addSeries(series)

        axis_x = QCategoryAxis()
        axis_x.append("Jan", 0)
        axis_x.append("Feb", 1)
        axis_x.append("Mar", 2)
        chart.addAxis(axis_x, Qt.AlignBottom)

        axis_y = QValueAxis()
        chart.addAxis(axis_y, Qt.AlignLeft)

        layout.addWidget(QChartView(chart))
        self.stats_tab.setLayout(layout)

    def _init_requests_tab(self):
        layout = QVBoxLayout()
        self.requests_table = QTableView()

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(
            ["IP", "Total"] + self._get_month_headers()
        )

        # Test data
        for i in range(5):
            row = [
                QStandardItem(f"192.168.1.{i}"),
                QStandardItem("100"),
                *[QStandardItem(str(i * 10)) for _ in range(3)],
            ]
            model.appendRow(row)

        self.requests_table.setModel(model)
        layout.addWidget(self.requests_table)
        self.requests_tab.setLayout(layout)

    def _init_failures_tab(self):
        layout = QVBoxLayout()
        chart = QChart()
        chart.setTitle("Denying stats")

        series = QBarSeries()
        bar_set = QBarSet("Denying")
        bar_set.append([10, 20, 15])
        series.append(bar_set)
        chart.addSeries(series)

        axis_x = QCategoryAxis()
        axis_x.append("404", 0)
        axis_x.append("500", 1)
        axis_x.append("503", 2)
        chart.addAxis(axis_x, Qt.AlignBottom)

        axis_y = QValueAxis()
        chart.addAxis(axis_y, Qt.AlignLeft)

        layout.addWidget(QChartView(chart))
        self.failures_tab.setLayout(layout)

    def _get_month_headers(self):
        return ["January", "February", "March"]