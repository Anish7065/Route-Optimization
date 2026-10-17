"""
Main Application Window.
"""
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QToolBar
from PySide6.QtGui import QAction
from core.graph import Graph
from database.db_manager import DatabaseManager
from gui.canvas import InteractiveCanvas
from gui.network_panel import NetworkControlPanel
from gui.algorithm_panel import AlgorithmControlPanel
from gui.results_panel import ResultsPanel
import config


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(config.APP_TITLE)
        self.resize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

        self.graph = Graph()
        self.db = DatabaseManager()

        self._init_ui()
        self._init_toolbar()

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Canvas
        self.canvas = InteractiveCanvas(self.graph)

        # Control Panels
        self.network_panel = NetworkControlPanel(self.graph, self._refresh_ui)
        self.algo_panel = AlgorithmControlPanel(self.graph, self._handle_algorithm_result)
        self.results_panel = ResultsPanel()

        left_sidebar = QVBoxLayout()
        left_sidebar.addWidget(self.network_panel)
        left_sidebar.addWidget(self.algo_panel)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.canvas, stretch=3)
        right_layout.addWidget(self.results_panel, stretch=1)

        main_layout.addLayout(left_sidebar, stretch=1)
        main_layout.addLayout(right_layout, stretch=3)

    def _init_toolbar(self):
        toolbar = QToolBar("Main Controls")
        self.addToolBar(toolbar)

        save_action = QAction("Save Network", self)
        save_action.triggered.connect(self._save_network)
        toolbar.addAction(save_action)

        load_action = QAction("Load Network", self)
        load_action.triggered.connect(self._load_network)
        toolbar.addAction(load_action)

        reset_action = QAction("Reset Network", self)
        reset_action.triggered.connect(self._reset_network)
        toolbar.addAction(reset_action)

    def _refresh_ui(self):
        self.canvas.redraw_network()
        self.network_panel.update_node_dropdowns()
        self.algo_panel.update_dropdowns()

    def _handle_algorithm_result(self, result):
        self.results_panel.display_result(result)
        if result.success:
            self.canvas.set_result_path(result.path, result.explored_nodes_order)

    def _save_network(self):
        self.db.save_graph(self.graph)

    def _load_network(self):
        self.graph = self.db.load_graph()
        self.canvas.graph = self.graph
        self.network_panel.graph = self.graph
        self.algo_panel.graph = self.graph
        self._refresh_ui()

    def _reset_network(self):
        self.graph.clear()
        self._refresh_ui()