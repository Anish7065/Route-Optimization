"""
Interactive QGraphicsView Canvas for Network Visualization and Construction.
"""
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem
from PySide6.QtCore import Qt, Signal, QPointF
from PySide6.QtGui import QPen, QBrush, QColor, QFont
from core.graph import Graph
from core.node import NodeType
import config


class InteractiveCanvas(QGraphicsView):
    node_selected = Signal(str)
    node_moved = Signal(str, float, float)

    def __init__(self, graph: Graph, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(self.renderHints())

        self.node_items = {}  # node_id -> QGraphicsEllipseItem
        self.edge_items = {}  # edge_id -> QGraphicsLineItem
        
        self.selected_node_id = None
        self.highlighted_path = []
        self.explored_nodes = []

        self.setBackgroundBrush(QBrush(QColor(config.COLOR_BACKGROUND)))

    def redraw_network(self):
        self.scene.clear()
        self.node_items.clear()
        self.edge_items.clear()

        # Draw Edges
        for edge_id, edge in self.graph.edges.items():
            src_node = self.graph.nodes[edge.source_id]
            tgt_node = self.graph.nodes[edge.target_id]

            line = self.scene.addLine(
                src_node.x, src_node.y, tgt_node.x, tgt_node.y,
                QPen(QColor(config.COLOR_EDGE), config.EDGE_WIDTH)
            )
            self.edge_items[edge_id] = line

            # Weight Label
            mid_x = (src_node.x + tgt_node.x) / 2
            mid_y = (src_node.y + tgt_node.y) / 2
            text = self.scene.addText(f"{edge.weight:.1f}")
            text.setDefaultTextColor(QColor("#BDC3C7"))
            text.setFont(QFont("Arial", 9, QFont.Bold))
            text.setPos(mid_x - 10, mid_y - 10)

        # Draw Nodes
        r = config.NODE_RADIUS
        for node_id, node in self.graph.nodes.items():
            color = QColor(config.COLOR_NODE_GENERIC)
            if node.node_type == NodeType.WAREHOUSE:
                color = QColor(config.COLOR_NODE_WAREHOUSE)
            elif node.node_type == NodeType.DELIVERY:
                color = QColor(config.COLOR_NODE_DELIVERY)

            if node_id == self.selected_node_id:
                color = QColor(config.COLOR_NODE_SELECTED)

            ellipse = self.scene.addEllipse(
                node.x - r, node.y - r, 2 * r, 2 * r,
                QPen(QColor("#FFFFFF"), 2),
                QBrush(color)
            )
            self.node_items[node_id] = ellipse

            label = self.scene.addText(node.name)
            label.setDefaultTextColor(QColor("#FFFFFF"))
            label.setFont(QFont("Arial", 10, QFont.Bold))
            label.setPos(node.x - r, node.y + r + 2)

        self._apply_path_highlights()

    def _apply_path_highlights(self):
        # Highlight calculated route
        if len(self.highlighted_path) > 1:
            for i in range(len(self.highlighted_path) - 1):
                u = self.highlighted_path[i]
                v = self.highlighted_path[i + 1]
                
                # Find matching edge ID
                for e_id, edge in self.graph.edges.items():
                    if (edge.source_id == u and edge.target_id == v) or \
                       (edge.is_bidirectional and edge.source_id == v and edge.target_id == u):
                        if e_id in self.edge_items:
                            self.edge_items[e_id].setPen(
                                QPen(QColor(config.COLOR_PATH), config.PATH_EDGE_WIDTH)
                            )

    def set_result_path(self, path: list, explored: list):
        self.highlighted_path = path
        self.explored_nodes = explored
        self.redraw_network()

    def mousePressEvent(self, event):
        scene_pos = self.mapToScene(event.pos())
        clicked_node_id = None

        # Check node intersection
        for node_id, node in self.graph.nodes.items():
            dx = scene_pos.x() - node.x
            dy = scene_pos.y() - node.y
            if dx * dx + dy * dy <= config.NODE_RADIUS * config.NODE_RADIUS:
                clicked_node_id = node_id
                break

        if clicked_node_id:
            self.selected_node_id = clicked_node_id
            self.node_selected.emit(clicked_node_id)
            self.redraw_network()
        else:
            super().mousePressEvent(event)