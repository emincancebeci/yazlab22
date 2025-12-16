import json
import csv


class Exporter:
    @staticmethod
    def export_graph_json(graph, path):
        data = {"nodes": [], "edges": []}

        for n in graph.nodes.values():
            data["nodes"].append(
                {
                    "id": n.id,
                    "name": n.name,
                    "aktiflik": n.aktiflik,
                    "etkilesim": n.etkilesim,
                    "baglantiSayisi": n.baglanti_sayisi,
                    "komsular": n.neighbors,
                }
            )

        for (u, v), e in graph.edges.items():
            data["edges"].append({"from": u, "to": v, "weight": e.weight})

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def export_graph_csv(graph, path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["DugumId", "Ozellik_I", "Ozellik_II", "Ozellik_III", "Komsular"])
            for n in graph.nodes.values():
                neighbors_str = ",".join(map(str, n.neighbors))
                writer.writerow([n.id, n.aktiflik, n.etkilesim, n.baglanti_sayisi, neighbors_str])

    @staticmethod
    def export_adjacency_list(graph, path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Node", "Neighbors"])
            for nid, neighbors in graph.adjacency_list().items():
                writer.writerow([nid, ",".join(map(str, neighbors))])

    @staticmethod
    def export_adjacency_matrix(graph, path):
        ids, matrix = graph.adjacency_matrix()
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([""] + ids)
            for nid, row in zip(ids, matrix):
                writer.writerow([nid] + row)
