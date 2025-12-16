import os
import time
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QTextEdit,
)
from core.algorithms import Algorithms
from core.node import Node
from io_.exporter import Exporter
from io_.loader import Loader
from .canvas import Canvas


class App(QMainWindow):
    def __init__(self, graph, initial_graph_path=None):
        super().__init__()

        self.graph = graph
        self.initial_graph_path = initial_graph_path
        self.setWindowTitle("Sosyal Ağ Analizi")
        self.resize(1200, 700)

        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.data_dir = os.path.join(self.base_dir, "data")
        os.makedirs(self.data_dir, exist_ok=True)

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        self.canvas = Canvas(self.graph, node_click_callback=self.on_node_clicked)
        main_layout.addWidget(self.canvas, stretch=3)

        panel = QWidget()
        panel_layout = QVBoxLayout(panel)

        self.start_input = QLineEdit()
        self.start_input.setPlaceholderText("Başlangıç node id")
        self.end_input = QLineEdit()
        self.end_input.setPlaceholderText("Bitiş node id")

        panel_layout.addWidget(QLabel("Başlangıç / Bitiş"))
        panel_layout.addWidget(self.start_input)
        panel_layout.addWidget(self.end_input)

        btn_bfs = QPushButton("BFS")
        btn_dfs = QPushButton("DFS")
        btn_dijkstra = QPushButton("En Kısa Yol (Dijkstra)")
        btn_astar = QPushButton("En Kısa Yol (A*)")
        btn_components = QPushButton("Bağlı Bileşenler")
        btn_degree = QPushButton("Derece Merkezilik (Top 5)")
        btn_welsh = QPushButton("Welsh-Powell Renklendirme")

        btn_bfs.clicked.connect(self.run_bfs)
        btn_dfs.clicked.connect(self.run_dfs)
        btn_dijkstra.clicked.connect(self.run_dijkstra)
        btn_astar.clicked.connect(self.run_astar)
        btn_components.clicked.connect(self.run_components)
        btn_degree.clicked.connect(self.run_degree)
        btn_welsh.clicked.connect(self.run_welsh)

        for btn in [btn_bfs, btn_dfs, btn_dijkstra, btn_astar, btn_components, btn_degree, btn_welsh]:
            panel_layout.addWidget(btn)

        panel_layout.addWidget(QLabel("Kullanıcı (Node) İşlemleri"))
        self.node_id_input = QLineEdit()
        self.node_id_input.setPlaceholderText("Node id")
        self.node_name_input = QLineEdit()
        self.node_name_input.setPlaceholderText("İsim")
        self.node_aktiflik_input = QLineEdit()
        self.node_aktiflik_input.setPlaceholderText("Aktiflik")
        self.node_etkilesim_input = QLineEdit()
        self.node_etkilesim_input.setPlaceholderText("Etkileşim")
        self.node_baglanti_input = QLineEdit()
        self.node_baglanti_input.setPlaceholderText("Bağlantı sayısı")

        for w in [
            self.node_id_input,
            self.node_name_input,
            self.node_aktiflik_input,
            self.node_etkilesim_input,
            self.node_baglanti_input,
        ]:
            panel_layout.addWidget(w)

        btn_node_add = QPushButton("Node Ekle")
        btn_node_update = QPushButton("Node Güncelle")
        btn_node_delete = QPushButton("Node Sil")
        btn_node_add.clicked.connect(self.add_node)
        btn_node_update.clicked.connect(self.update_node)
        btn_node_delete.clicked.connect(self.delete_node)
        for btn in [btn_node_add, btn_node_update, btn_node_delete]:
            panel_layout.addWidget(btn)

        panel_layout.addWidget(QLabel("Bağlantı (Edge) İşlemleri"))
        self.edge_u_input = QLineEdit()
        self.edge_u_input.setPlaceholderText("Kaynak id (u)")
        self.edge_v_input = QLineEdit()
        self.edge_v_input.setPlaceholderText("Hedef id (v)")
        panel_layout.addWidget(self.edge_u_input)
        panel_layout.addWidget(self.edge_v_input)

        btn_edge_add = QPushButton("Edge Ekle")
        btn_edge_delete = QPushButton("Edge Sil")
        btn_edge_add.clicked.connect(self.add_edge)
        btn_edge_delete.clicked.connect(self.delete_edge)
        for btn in [btn_edge_add, btn_edge_delete]:
            panel_layout.addWidget(btn)

        btn_export_json = QPushButton("JSON dışa aktar")
        btn_export_csv = QPushButton("CSV dışa aktar")
        btn_adj_list = QPushButton("Komşuluk listesi CSV")
        btn_adj_matrix = QPushButton("Komşuluk matrisi CSV")
        btn_import_json = QPushButton("JSON içe aktar (graph_export.json)")
        btn_import_csv = QPushButton("CSV içe aktar (graph_export.csv)")
        btn_reset = QPushButton("Başlangıç grafına dön")

        btn_export_json.clicked.connect(self.export_json)
        btn_export_csv.clicked.connect(self.export_csv)
        btn_adj_list.clicked.connect(self.export_adj_list)
        btn_adj_matrix.clicked.connect(self.export_adj_matrix)
        btn_import_json.clicked.connect(self.import_json)
        btn_import_csv.clicked.connect(self.import_csv)
        btn_reset.clicked.connect(self.reset_graph)

        panel_layout.addWidget(QLabel("Veri içe/dışa aktarım"))
        for btn in [
            btn_export_json,
            btn_export_csv,
            btn_adj_list,
            btn_adj_matrix,
            btn_import_json,
            btn_import_csv,
            btn_reset,
        ]:
            panel_layout.addWidget(btn)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        panel_layout.addWidget(QLabel("Sonuç"))
        panel_layout.addWidget(self.result)
        panel_layout.addStretch()

        main_layout.addWidget(panel, stretch=1)

        self.setCentralWidget(main_widget)

        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #121212;
            }
            QWidget {
                background-color: #121212;
                color: #f0f0f0;
            }
            QLineEdit, QTextEdit {
                background-color: #1f1f1f;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 4px;
                color: #f0f0f0;
            }
            QPushButton {
                background-color: #2d2d2d;
                border-radius: 4px;
                padding: 6px 10px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
            QPushButton:pressed {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #f0f0f0;
            }
            """
        )

    def _parse_int(self, text):
        try:
            return int(text)
        except Exception:
            return None

    def _parse_float(self, text, default=0.0):
        try:
            if text.strip() == "":
                return default
            return float(text)
        except Exception:
            return default

    def _set_result(self, message):
        self.result.setPlainText(message)

    def _refresh_canvas(self):
        self.canvas.graph = self.graph
        self.canvas.clear_path()
        self.canvas.set_colors({})
        self.canvas.update()

    def on_node_clicked(self, node_id):
        node = self.graph.nodes.get(node_id)
        if not node:
            return
        info_lines = [
            f"Seçilen Node: {node.id} - {node.name}",
            f"Aktiflik: {node.aktiflik}",
            f"Etkileşim: {node.etkilesim}",
            f"Bağlantı sayısı: {node.baglanti_sayisi}",
            f"Komşular: {node.neighbors}",
        ]
        self.canvas.set_path([node.id])
        self._set_result("\n".join(info_lines))

    def add_node(self):
        nid = self._parse_int(self.node_id_input.text())
        if nid is None:
            self._set_result("Geçerli bir node id gir.")
            return
        if nid in self.graph.nodes:
            self._set_result("Bu id'ye sahip node zaten var.")
            return
        name = self.node_name_input.text().strip() or f"Node{nid}"
        aktiflik = self._parse_float(self.node_aktiflik_input.text(), 0.0)
        etkilesim = self._parse_float(self.node_etkilesim_input.text(), 0.0)
        baglanti = self._parse_float(self.node_baglanti_input.text(), 0.0)
        node = Node(nid, name, aktiflik, etkilesim, baglanti)
        try:
            self.graph.add_node(node)
        except Exception as e:
            self._set_result(f"Node eklenemedi: {e}")
            return
        self._refresh_canvas()
        self._set_result(f"Node eklendi: {nid}")

    def update_node(self):
        nid = self._parse_int(self.node_id_input.text())
        if nid is None or nid not in self.graph.nodes:
            self._set_result("Güncellenecek geçerli bir node id gir.")
            return
        node = self.graph.nodes[nid]
        name = self.node_name_input.text().strip() or node.name
        aktiflik = self._parse_float(self.node_aktiflik_input.text(), node.aktiflik)
        etkilesim = self._parse_float(self.node_etkilesim_input.text(), node.etkilesim)
        baglanti = self._parse_float(self.node_baglanti_input.text(), node.baglanti_sayisi)
        node.name = name
        node.aktiflik = aktiflik
        node.etkilesim = etkilesim
        node.baglanti_sayisi = baglanti
        if hasattr(self.graph, "recalculate_weights_for_node"):
            self.graph.recalculate_weights_for_node(nid)
        self._refresh_canvas()
        self._set_result(f"Node güncellendi: {nid}")

    def delete_node(self):
        nid = self._parse_int(self.node_id_input.text())
        if nid is None or nid not in self.graph.nodes:
            self._set_result("Silinecek geçerli bir node id gir.")
            return
        self.graph.remove_node(nid)
        self._refresh_canvas()
        self._set_result(f"Node silindi: {nid}")

    def add_edge(self):
        u = self._parse_int(self.edge_u_input.text())
        v = self._parse_int(self.edge_v_input.text())
        if u is None or v is None:
            self._set_result("u ve v id'lerini gir.")
            return
        try:
            self.graph.add_edge(u, v)
        except Exception as e:
            self._set_result(f"Edge eklenemedi: {e}")
            return
        self._refresh_canvas()
        self._set_result(f"Edge eklendi: {u} - {v}")

    def delete_edge(self):
        u = self._parse_int(self.edge_u_input.text())
        v = self._parse_int(self.edge_v_input.text())
        if u is None or v is None:
            self._set_result("u ve v id'lerini gir.")
            return
        self.graph.remove_edge(u, v)
        self._refresh_canvas()
        self._set_result(f"Edge silindi: {u} - {v}")

    def run_bfs(self):
        start = self._parse_int(self.start_input.text())
        if start is None or start not in self.graph.nodes:
            self._set_result("Geçerli bir başlangıç id gir.")
            return
        self.canvas.clear_path()
        self.canvas.set_colors({})
        t0 = time.perf_counter()
        visited = Algorithms.bfs(self.graph, start)
        t1 = time.perf_counter()
        elapsed = (t1 - t0) * 1000
        self._set_result(f"BFS sırası: {visited}\nSüre: {elapsed:.2f} ms")

    def run_dfs(self):
        start = self._parse_int(self.start_input.text())
        if start is None or start not in self.graph.nodes:
            self._set_result("Geçerli bir başlangıç id gir.")
            return
        self.canvas.clear_path()
        self.canvas.set_colors({})
        t0 = time.perf_counter()
        visited = Algorithms.dfs(self.graph, start, [])
        t1 = time.perf_counter()
        elapsed = (t1 - t0) * 1000
        self._set_result(f"DFS sırası: {visited}\nSüre: {elapsed:.2f} ms")

    def run_dijkstra(self):
        start = self._parse_int(self.start_input.text())
        end = self._parse_int(self.end_input.text())
        if start is None or end is None:
            self._set_result("Başlangıç ve bitiş id gir.")
            return
        t0 = time.perf_counter()
        path, dist = Algorithms.dijkstra(self.graph, start, end)
        t1 = time.perf_counter()
        elapsed = (t1 - t0) * 1000
        if not path:
            self.canvas.clear_path()
            self._set_result("Yol bulunamadı.")
            return
        self.canvas.set_path(path)
        self._set_result(f"Dijkstra yol: {path} | Maliyet: {dist:.4f}\nSüre: {elapsed:.2f} ms")

    def run_astar(self):
        start = self._parse_int(self.start_input.text())
        end = self._parse_int(self.end_input.text())
        if start is None or end is None:
            self._set_result("Başlangıç ve bitiş id gir.")
            return
        t0 = time.perf_counter()
        path, dist = Algorithms.a_star(self.graph, start, end)
        t1 = time.perf_counter()
        elapsed = (t1 - t0) * 1000
        if not path:
            self.canvas.clear_path()
            self._set_result("Yol bulunamadı.")
            return
        self.canvas.set_path(path)
        self._set_result(f"A* yol: {path} | Maliyet: {dist:.4f}\nSüre: {elapsed:.2f} ms")

    def run_components(self):
        t0 = time.perf_counter()
        comps = Algorithms.connected_components(self.graph)
        t1 = time.perf_counter()
        elapsed = (t1 - t0) * 1000
        self.canvas.clear_path()
        color_map = {}
        for cid, comp in enumerate(comps):
            for nid in comp:
                color_map[nid] = cid
        self.canvas.set_colors(color_map)
        lines = []
        for i, c in enumerate(comps):
            lines.append(f"{i+1}. bileşen (boyut {len(c)}): {c}")
        lines.append(f"Süre: {elapsed:.2f} ms")
        self._set_result("\n".join(lines))

    def run_degree(self):
        t0 = time.perf_counter()
        centrality = Algorithms.degree_centrality(self.graph, top_n=5)
        t1 = time.perf_counter()
        elapsed = (t1 - t0) * 1000
        self.canvas.clear_path()
        color_map = {}
        for idx, (nid, _deg) in enumerate(centrality):
            color_map[nid] = idx
        self.canvas.set_colors(color_map)
        lines = ["Node\tDerece"]
        for nid, deg in centrality:
            lines.append(f"{nid}\t{deg}")
        lines.append(f"Süre: {elapsed:.2f} ms")
        self._set_result("\n".join(lines))

    def run_welsh(self):
        t0 = time.perf_counter()
        colors = Algorithms.welsh_powell(self.graph)
        t1 = time.perf_counter()
        elapsed = (t1 - t0) * 1000
        self.canvas.clear_path()
        self.canvas.set_colors(colors)
        lines = [f"Node {nid} -> Renk {color}" for nid, color in colors.items()]
        lines.append(f"Süre: {elapsed:.2f} ms")
        self._set_result("\n".join(lines))

    def export_json(self):
        path = os.path.join(self.data_dir, "graph_export.json")
        Exporter.export_graph_json(self.graph, path)
        self._set_result(f"JSON kaydedildi: {path}")

    def export_csv(self):
        path = os.path.join(self.data_dir, "graph_export.csv")
        Exporter.export_graph_csv(self.graph, path)
        self._set_result(f"CSV kaydedildi: {path}")

    def export_adj_list(self):
        path = os.path.join(self.data_dir, "adjacency_list.csv")
        Exporter.export_adjacency_list(self.graph, path)
        self._set_result(f"Komşuluk listesi kaydedildi: {path}")

    def export_adj_matrix(self):
        path = os.path.join(self.data_dir, "adjacency_matrix.csv")
        Exporter.export_adjacency_matrix(self.graph, path)
        self._set_result(f"Komşuluk matrisi kaydedildi: {path}")

    def import_json(self):
        path = os.path.join(self.data_dir, "graph_export.json")
        try:
            g = Loader.load_graph_from_json(path)
        except Exception as e:
            self._set_result(f"JSON içe aktarılamadı: {e}")
            return
        self.graph = g
        self._refresh_canvas()
        self._set_result(f"JSON'dan grafik yüklendi: {path}")

    def import_csv(self):
        path = os.path.join(self.data_dir, "graph_export.csv")
        try:
            g = Loader.load_graph_from_csv(path)
        except Exception as e:
            self._set_result(f"CSV içe aktarılamadı: {e}")
            return
        self.graph = g
        self._refresh_canvas()
        self._set_result(f"CSV'den grafik yüklendi: {path}")

    def reset_graph(self):
        if not self.initial_graph_path:
            self._set_result("Başlangıç grafı yolu tanımlı değil.")
            return
        try:
            g = Loader.load_graph_from_json(self.initial_graph_path)
        except Exception as e:
            self._set_result(f"Başlangıç grafı yüklenemedi: {e}")
            return
        self.graph = g
        self._refresh_canvas()
        self._set_result(f"Başlangıç grafına dönüldü: {self.initial_graph_path}")
