from .node import Node
from .edge import Edge
from .weight import calculate_weight

class Graph:
    def __init__(self):
        self.nodes = {}  # {id: Node}
        self.edges = {}  # {(u, v): Edge}

    # --- NODE OPERASYONLARI ---
    def add_node(self, node: Node):
        if node.id in self.nodes:
            raise ValueError("Node already exists.")
        self.nodes[node.id] = node

    def remove_node(self, node_id):
        if node_id not in self.nodes:
            return
        del self.nodes[node_id]

        # ilişkili kenarları sil
        self.edges = {k: e for k, e in self.edges.items() if node_id not in k}

    # --- EDGE OPERASYONLARI ---
    def add_edge(self, u, v):
        if u not in self.nodes or v not in self.nodes:
            raise ValueError("Node not found.")

        if u == v:
            raise ValueError("Self-loop edge is not allowed.")

        if (u, v) in self.edges or (v, u) in self.edges:
            raise ValueError("Edge already exists.")

        n1, n2 = self.nodes[u], self.nodes[v]
        w = calculate_weight(n1, n2)

        edge = Edge(u, v, w)
        self.edges[(u, v)] = edge
        self.edges[(v, u)] = edge  # yönsüz grafik

        n1.add_neighbor(v)
        n2.add_neighbor(u)

    def remove_edge(self, u, v):
        if (u, v) in self.edges:
            del self.edges[(u, v)]
        if (v, u) in self.edges:
            del self.edges[(v, u)]
