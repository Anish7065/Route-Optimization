"""
Side Panel for Node & Road Network Controls.
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QFormLayout, 
                             QLineEdit, QComboBox, QPushButton, QDoubleSpinBox, QMessageBox)
from core.graph import Graph
from core.node import Node, NodeType
from core.edge import Edge


class NetworkControlPanel(QWidget):
    def __init__(self, graph: Graph, canvas_refresh_cb, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.refresh_canvas = canvas_refresh_cb

        layout = QVBoxLayout(self)

        # Add Node Group
        node_group = QGroupBox("Add Node")
        node_form = QFormLayout(node_group)
        self.node_id_input = QLineEdit()
        self.node_name_input = QLineEdit()
        self.node_type_combo = QComboBox()
        self.node_type_combo.addItems(["Generic", "Warehouse", "Delivery"])
        self.node_x_input = QDoubleSpinBox()
        self.node_x_input.setRange(0, 2000)
        self.node_x_input.setValue(100)
        self.node_y_input = QDoubleSpinBox()
        self.node_y_input.setRange(0, 2000)
        self.node_y_input.setValue(100)

        add_node_btn = QPushButton("Add Node")
        add_node_btn.clicked.connect(self._handle_add_node)

        node_form.addRow("Node ID:", self.node_id_input)
        node_form.addRow("Name:", self.node_name_input)
        node_form.addRow("Type:", self.node_type_combo)
        node_form.addRow("X:", self.node_x_input)
        node_form.addRow("Y:", self.node_y_input)
        node_form.addRow(add_node_btn)
        layout.addWidget(node_group)

        # Add Road Group
        road_group = QGroupBox("Add/Update Road")
        road_form = QFormLayout(road_group)
        self.src_combo = QComboBox()
        self.tgt_combo = QComboBox()
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(0.1, 10000.0)
        self.weight_input.setValue(10.0)

        add_road_btn = QPushButton("Connect Nodes")
        add_road_btn.clicked.connect(self._handle_add_road)

        road_form.addRow("Source:", self.src_combo)
        road_form.addRow("Target:", self.tgt_combo)
        road_form.addRow("Weight/Dist:", self.weight_input)
        road_form.addRow(add_road_btn)
        layout.addWidget(road_group)

        # Management Buttons
        delete_btn = QPushButton("Delete Selected Node")
        delete_btn.clicked.connect(self._handle_delete_node)
        layout.addWidget(delete_btn)

        layout.addStretch()

    def update_node_dropdowns(self):
        nodes = list(self.graph.nodes.keys())
        self.src_combo.clear()
        self.tgt_combo.clear()
        self.src_combo.addItems(nodes)
        self.tgt_combo.addItems(nodes)

    def _handle_add_node(self):
        n_id = self.node_id_input.text().strip()
        n_name = self.node_name_input.text().strip() or n_id
        n_type_str = self.node_type_combo.currentText().lower()

        if not n_id:
            QMessageBox.warning(self, "Validation Error", "Node ID cannot be empty.")
            return

        try:
            node_type = NodeType(n_type_str)
            node = Node(id=n_id, name=n_name, x=self.node_x_input.value(), y=self.node_y_input.value(), node_type=node_type)
            self.graph.add_node(node)
            self.update_node_dropdowns()
            self.refresh_canvas()
            self.node_id_input.clear()
            self.node_name_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _handle_add_road(self):
        u = self.src_combo.currentText()
        v = self.tgt_combo.currentText()
        w = self.weight_input.value()

        if not u or not v or u == v:
            QMessageBox.warning(self, "Validation Error", "Select two distinct valid nodes.")
            return

        edge_id = f"e_{u}_{v}"
        try:
            edge = Edge(id=edge_id, source_id=u, target_id=v, weight=w)
            self.graph.add_edge(edge)
            self.refresh_canvas()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _handle_delete_node(self):
        # Triggered via canvas selection
        pass