"""
Performance Telemetry and Output Display Panel.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel, QTextEdit
from algorithms.base import AlgorithmResult


class ResultsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        group = QGroupBox("Execution Metrics & Results")
        group_layout = QVBoxLayout(group)

        self.status_label = QLabel("Status: Ready")
        self.metrics_label = QLabel("Distance: N/A | Time: N/A | Explored Nodes: N/A")
        self.path_display = QTextEdit()
        self.path_display.setReadOnly(True)

        group_layout.addWidget(self.status_label)
        group_layout.addWidget(self.metrics_label)
        group_layout.addWidget(self.path_display)

        layout.addWidget(group)

    def display_result(self, result: AlgorithmResult):
        if not result.success:
            self.status_label.setText(f"Status: Failed ({result.error_message})")
            self.metrics_label.setText("Distance: ∞ | Time: 0.0 ms | Explored Nodes: 0")
            self.path_display.setText("No path found.")
            return

        self.status_label.setText(f"Status: Success ({result.algorithm_name})")
        self.metrics_label.setText(
            f"Distance: {result.total_distance:.2f} units | "
            f"Time: {result.execution_time_ms:.3f} ms | "
            f"Explored: {result.nodes_explored} nodes"
        )
        self.path_display.setText(" → ".join(result.path))