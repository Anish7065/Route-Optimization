"""
Domain models for Network Nodes.
"""
from dataclasses import dataclass
from enum import Enum
import math


class NodeType(Enum):
    GENERIC = "generic"
    WAREHOUSE = "warehouse"
    DELIVERY = "delivery"


@dataclass
class Node:
    id: str
    name: str
    x: float
    y: float
    node_type: NodeType = NodeType.GENERIC

    def euclidean_distance(self, other: "Node") -> float:
        """Calculate straight-line distance between two nodes."""
        return math.hypot(self.x - other.x, self.y - other.y)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "node_type": self.node_type.value,
            "x": self.x,
            "y": self.y,
        }