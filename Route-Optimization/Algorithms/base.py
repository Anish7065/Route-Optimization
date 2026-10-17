"""
Abstract Interface for Route Algorithms & Performance Result Wrapper.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from core.graph import Graph


@dataclass
class AlgorithmResult:
    algorithm_name: str
    path: List[str] = field(default_factory=list)
    total_distance: float = float("inf")
    nodes_explored: int = 0
    edges_examined: int = 0
    execution_time_ms: float = 0.0
    explored_nodes_order: List[str] = field(default_factory=list)
    success: bool = False
    error_message: Optional[str] = None


class RouteAlgorithm(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def run(self, graph: Graph, source_id: str, destination_id: str) -> AlgorithmResult:
        pass