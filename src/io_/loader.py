import json
import csv
from core.node import Node
from core.graph import Graph


class Loader:
    @staticmethod
    def load_graph_from_json(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        g = Graph()

        for n in data["nodes"]:
            node = Node(n["id"], n["name"], n["aktiflik"], n["etkilesim"], n["baglantiSayisi"])
            g.add_node(node)

        for e in data["edges"]:
            g.add_edge(e["from"], e["to"])

        return g
