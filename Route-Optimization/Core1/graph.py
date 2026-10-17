"""
Graph Data Structure using Adjacency List.
"""
from typing import Dict, List, Optional, Tuple
from core.node import Node, NodeType
from core.edge import Edge


class Graph:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        # Adjacency list: node_id -> List[Tuple[neighbor_id, weight, edge_id]]
        self.adjacency: Dict[str, List[Tuple[str, float, str]]] = {}
        self.edges: Dict[str, Edge] = {}

    def add_node(self, node: Node) -> None:
        if node.id in self.nodes:
            raise ValueError(f"Node '{node.id}' already exists.")
        self.nodes[node.id] = node
        self.adjacency[node.id] = []

    def remove_node(self, node_id: str) -> None:
        if node_id not in self.nodes:
            return
        
        # Remove associated edges
        edges_to_remove = [
            e_id for e_id, edge in self.edges.items()
            if edge.source_id == node_id or edge.target_id == node_id
        ]
        for e_id in edges_to_remove:
            self.remove_edge(e_id)

        del self.nodes[node_id]
        del self.adjacency[node_id]

    def add_edge(self, edge: Edge) -> None:
        if edge.source_id not in self.nodes or edge.target_id not in self.nodes:
            raise KeyError("Both source and target nodes must exist in the graph.")
        
        self.edges[edge.id] = edge
        self.adjacency[edge.source_id].append((edge.target_id, edge.weight, edge.id))
        
        if edge.is_bidirectional:
            self.adjacency[edge.target_id].append((edge.source_id, edge.weight, edge.id))

    def remove_edge(self, edge_id: str) -> None:
        if edge_id not in self.edges:
            return
        
        edge = self.edges[edge_id]
        self.adjacency[edge.source_id] = [
            item for item in self.adjacency[edge.source_id] if item[2] != edge_id
        ]
        if edge.is_bidirectional:
            self.adjacency[edge.target_id] = [
                item for item in self.adjacency[edge.target_id] if item[2] != edge_id
            ]
        del self.edges[edge_id]

    def update_edge_weight(self, edge_id: str, new_weight: float) -> None:
        if edge_id not in self.edges:
            raise KeyError(f"Edge '{edge_id}' does not exist.")
        if new_weight < 0:
            raise ValueError("Edge weight cannot be negative.")
        
        edge = self.edges[edge_id]
        edge.weight = new_weight
        
        # Update in adjacency list
        self.remove_edge(edge_id)
        self.add_edge(edge)

    def get_neighbors(self, node_id: str) -> List[Tuple[str, float, str]]:
        return self.adjacency.get(node_id, [])

    def clear(self) -> None:
        self.nodes.clear()
        self.adjacency.clear()
        self.edges.clear()