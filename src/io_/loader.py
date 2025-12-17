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

    @staticmethod
    def load_graph_from_csv(path):
        """
        Beklenen kolonlar: DugumId, Ozellik_I, Ozellik_II, Ozellik_III, Komsular
        Komsular virgülle ayrılmış id listesi.
        """
        g = Graph()
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        for row in rows:
            node_id = int(row["DugumId"])
            aktiflik = float(row["Ozellik_I"])
            etkilesim = float(row["Ozellik_II"])
            baglanti = float(row["Ozellik_III"])
            node = Node(node_id, str(node_id), aktiflik, etkilesim, baglanti)
            g.add_node(node)

        # edges from neighbors column; avoid duplicates by only adding u<v
        for row in rows:
            u = int(row["DugumId"])
            neighbors_str = row.get("Komsular", "")
            if not neighbors_str:
                continue
            for v_str in neighbors_str.split(","):
                if not v_str.strip():
                    continue
                v = int(v_str)
                if u < v and u in g.nodes and v in g.nodes:
                    try:
                        g.add_edge(u, v)
                    except ValueError:
                        # duplicate/self-loop guard already inside
                        pass

        return g
