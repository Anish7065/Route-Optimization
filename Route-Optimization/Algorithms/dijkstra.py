"""
Dijkstra's Shortest Path Algorithm Implementation.
"""
import heapq
import time
from typing import Dict, List, Optional
from core.graph import Graph
from algorithms.base import RouteAlgorithm, AlgorithmResult


class DijkstraAlgorithm(RouteAlgorithm):
    @property
    def name(self) -> str:
        return "Dijkstra"

    def run(self, graph: Graph, source_id: str, destination_id: str) -> AlgorithmResult:
        start_time = time.perf_counter()
        
        if source_id not in graph.nodes or destination_id not in graph.nodes:
            return AlgorithmResult(
                algorithm_name=self.name,
                success=False,
                error_message="Source or Destination node does not exist in graph."
            )

        distances: Dict[str, float] = {node_id: float("inf") for node_id in graph.nodes}
        previous: Dict[str, Optional[str]] = {node_id: None for node_id in graph.nodes}
        distances[source_id] = 0.0

        # Min-priority queue: (distance, node_id)
        pq = [(0.0, source_id)]
        visited = set()
        explored_order = []
        edges_examined = 0

        while pq:
            current_dist, current_node = heapq.heappop(pq)

            if current_node in visited:
                continue
            
            visited.add(current_node)
            explored_order.append(current_node)

            if current_node == destination_id:
                break

            for neighbor_id, weight, _ in graph.get_neighbors(current_node):
                edges_examined += 1
                if neighbor_id in visited:
                    continue

                new_dist = current_dist + weight
                if new_dist < distances[neighbor_id]:
                    distances[neighbor_id] = new_dist
                    previous[neighbor_id] = current_node
                    heapq.heappush(pq, (new_dist, neighbor_id))

        exec_time = (time.perf_counter() - start_time) * 1000.0

        if distances[destination_id] == float("inf"):
            return AlgorithmResult(
                algorithm_name=self.name,
                nodes_explored=len(visited),
                edges_examined=edges_examined,
                execution_time_ms=exec_time,
                explored_nodes_order=explored_order,
                success=False,
                error_message="No path exists between source and destination."
            )

        # Reconstruct path
        path = []
        curr = destination_id
        while curr is not None:
            path.append(curr)
            curr = previous[curr]
        path.reverse()

        return AlgorithmResult(
            algorithm_name=self.name,
            path=path,
            total_distance=distances[destination_id],
            nodes_explored=len(visited),
            edges_examined=edges_examined,
            execution_time_ms=exec_time,
            explored_nodes_order=explored_order,
            success=True
        )