from core.graph import Graph
from core.node import Node

def test_graph():
    g = Graph()
    g.add_node(Node(1, "Ali"))
    g.add_node(Node(2, "Veli"))
    g.add_edge(1, 2)

    assert 1 in g.nodes
    assert 2 in g.nodes
    assert (1, 2) in g.edges
