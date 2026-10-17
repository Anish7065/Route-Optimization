"""
Database Persistence Manager using SQLite.
"""
import sqlite3
from typing import Optional
from core.graph import Graph
from core.node import Node, NodeType
from core.edge import Edge


class DatabaseManager:
    def __init__(self, db_path: str = "routex.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS nodes (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    node_type TEXT NOT NULL,
                    x REAL NOT NULL,
                    y REAL NOT NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS roads (
                    id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    weight REAL NOT NULL,
                    is_bidirectional INTEGER NOT NULL,
                    FOREIGN KEY(source_id) REFERENCES nodes(id) ON DELETE CASCADE,
                    FOREIGN KEY(target_id) REFERENCES nodes(id) ON DELETE CASCADE
                );
            """)
            conn.commit()

    def save_graph(self, graph: Graph) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM roads;")
            cursor.execute("DELETE FROM nodes;")

            for node in graph.nodes.values():
                cursor.execute(
                    "INSERT INTO nodes (id, name, node_type, x, y) VALUES (?, ?, ?, ?, ?);",
                    (node.id, node.name, node.node_type.value, node.x, node.y)
                )

            for edge in graph.edges.values():
                cursor.execute(
                    "INSERT INTO roads (id, source_id, target_id, weight, is_bidirectional) VALUES (?, ?, ?, ?, ?);",
                    (edge.id, edge.source_id, edge.target_id, edge.weight, 1 if edge.is_bidirectional else 0)
                )
            conn.commit()

    def load_graph(self) -> Graph:
        graph = Graph()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, node_type, x, y FROM nodes;")
            for row in cursor.fetchall():
                node = Node(
                    id=row[0],
                    name=row[1],
                    node_type=NodeType(row[2]),
                    x=row[3],
                    y=row[4]
                )
                graph.add_node(node)

            cursor.execute("SELECT id, source_id, target_id, weight, is_bidirectional FROM roads;")
            for row in cursor.fetchall():
                edge = Edge(
                    id=row[0],
                    source_id=row[1],
                    target_id=row[2],
                    weight=row[3],
                    is_bidirectional=bool(row[4])
                )
                graph.add_edge(edge)
        return graph