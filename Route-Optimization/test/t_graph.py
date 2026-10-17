"""
Unit Tests for Graph, Node, and Edge domain constructs.
"""
import pytest
from core.graph import Graph
from core.node import Node, NodeType
from core.edge import Edge


def test_add_and_remove_node():
    g = Graph()
    n1 = Node("n1", "Node 1", 0.0, 0.0)
    g.add_node(n1)

    assert "n1" in g.nodes
    assert len(g.nodes) == 1

    g.remove_node("n1")
    assert "n1" not in g.nodes
    assert len(g.nodes) == 0


def test_add_edge_missing_nodes():
    g = Graph()
    e = Edge("e1", "n1", "n2", 10.0)
    with pytest.raises(KeyError):
        g.add_edge(e)