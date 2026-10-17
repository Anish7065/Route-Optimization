"""
Unit Tests for Dijkstra and A* Routing Algorithms.
"""
from core.graph import Graph
from core.node import Node
from core.edge import Edge
from algorithms.dijkstra import DijkstraAlgorithm
from algorithms.astar import AStarAlgorithm


def create_sample_graph():
    g = Graph()
    g.add_node(Node("A", "A", 0, 0))
    g.add_node(Node("B", "B", 10, 0))
    g.add_node(Node("C", "C", 5, 5))

    g.add_edge(Edge("e1", "A", "B", 10.0))
    g.add_edge(Edge("e2", "A", "C", 3.0))
    g.add_edge(Edge("e3", "C", "B", 2.0))
    return g


def test_dijkstra():
    g = create_sample_graph()
    algo = DijkstraAlgorithm()
    res = algo.run(g, "A", "B")

    assert res.success is True
    assert res.path == ["A", "C", "B"]
    assert res.total_distance == 5.0


def test_astar():
    g = create_sample_graph()
    algo = AStarAlgorithm()
    res = algo.run(g, "A", "B")

    assert res.success is True
    assert res.path == ["A", "C", "B"]
    assert res.total_distance == 5.0