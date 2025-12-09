import json
from io_.exporter import Exporter

class Exporter:
    @staticmethod
    def export_graph(graph, path):
        data = {
            "nodes": [],
            "edges": []
        }

        for n in graph.nodes.values():
            data["nodes"].append({
                "id": n.id,
                "name": n.name,
                "aktiflik": n.aktiflik,
                "etkilesim": n.etkilesim,
                "baglantiSayisi": n.baglanti_sayisi,
                "komsular": n.neighbors
            })

        for (u, v), e in graph.edges.items():
            data["edges"].append({
                "from": u,
                "to": v,
                "weight": e.weight
            })

        with open(path, "w") as f:
            json.dump(data, f, indent=4)
