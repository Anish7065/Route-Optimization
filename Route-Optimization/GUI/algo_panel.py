"""
Algorithm Selection and Execution Panel.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QComboBox, QPushButton, QMessageBox
from core.graph import Graph
from algorithms.dijkstra import DijkstraAlgorithm
from algorithms.astar import AStarAlgorithm


class AlgorithmControlPanel(QWidget):
    def __init__(self, graph: Graph, execution_callback, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.execute_cb = execution_callback

        self.algorithms = {
            "Dijkstra": DijkstraAlgorithm(),
            "A* Search": AStarAlgorithm()
        }

        layout = QVBoxLayout(self)
        group = QGroupBox("Algorithm Execution")
        form = QFormLayout(group)

        self.algo_combo = QComboBox()
        self.algo_combo.addItems(list(self.algorithms.keys()))

        self.src_combo = QComboBox()
        self.dst_combo = QComboBox()

        run_btn = QPushButton("Run Route Optimization")
        run_btn.clicked.connect(self._handle_run)

        form.addRow("Algorithm:", self.algo_combo)
        form.addRow("Source:", self.src_combo)
        form.addRow("Destination:", self.dst_combo)
        form.addRow(run_btn)

        layout.addWidget(group)

    def update_dropdowns(self):
        nodes = list(self.graph.nodes.keys())
        self.src_combo.clear()
        self.dst_combo.clear()
        self.src_combo.addItems(nodes)
        self.dst_combo.addItems(nodes)

    def _handle_run(self):
        algo_name = self.algo_combo.currentText()
        src = self.src_combo.currentText()
        dst = self.dst_combo.currentText()

        if not src or not dst:
            QMessageBox.warning(self, "Error", "Select valid Source and Destination nodes.")
            return

        algo = self.algorithms[algo_name]
        result = algo.run(self.graph, src, dst)
        self.execute_cb(result)