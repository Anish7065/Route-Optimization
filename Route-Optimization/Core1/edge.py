"""
Domain model for Network Edges (Roads).
"""
from dataclasses import dataclass


@dataclass
class Edge:
    id: str
    source_id: str
    target_id: str
    weight: float
    is_bidirectional: bool = True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "weight": self.weight,
            "is_bidirectional": self.is_bidirectional,
        }