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
    QScrollArea,
    QSplitter,
    QFileDialog,
    QMessageBox,
)
from PyQt5.QtCore import Qt
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
        self.resize(1400, 800)

        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.data_dir = os.path.join(self.base_dir, "data")
        os.makedirs(self.data_dir, exist_ok=True)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        splitter = QSplitter(Qt.Horizontal)

        self.canvas = Canvas(self.graph, node_click_callback=self.on_node_clicked)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.canvas)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #121212; }")

        splitter.addWidget(scroll_area)

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
        btn_dijkstra = QPushButton("Dijkstra (En kısa yol)")
        btn_astar = QPushButton("A* (En kısa yol)")
        btn_components = QPushButton("Bağlı bileşenler")
        btn_degree = QPushButton("Derece (Top 5)")
        btn_welsh = QPushButton("Welsh-Powell renk")

        btn_bfs.clicked.connect(self.run_bfs)
        btn_dfs.clicked.connect(self.run_dfs)
        btn_dijkstra.clicked.connect(self.run_dijkstra)
        btn_astar.clicked.connect(self.run_astar)
        btn_components.clicked.connect(self.run_components)
        btn_degree.clicked.connect(self.run_degree)
        btn_welsh.clicked.connect(self.run_welsh)

        algo_buttons = [btn_bfs, btn_dfs, btn_dijkstra, btn_astar, btn_components, btn_degree, btn_welsh]
        for btn in algo_buttons:
            btn.setMinimumHeight(30)
            btn.setMinimumWidth(220)
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

        node_inputs = [
            self.node_id_input,
            self.node_name_input,
            self.node_aktiflik_input,
            self.node_etkilesim_input,
            self.node_baglanti_input,
        ]
        for w in node_inputs:
            w.setMinimumHeight(26)
            w.setMinimumWidth(220)
            panel_layout.addWidget(w)

        btn_node_add = QPushButton("Node ekle")
        btn_node_update = QPushButton("Node güncelle")
        btn_node_delete = QPushButton("Node sil")
        btn_node_add.clicked.connect(self.add_node)
        btn_node_update.clicked.connect(self.update_node)
        btn_node_delete.clicked.connect(self.delete_node)
        node_buttons = [btn_node_add, btn_node_update, btn_node_delete]
        for btn in node_buttons:
            btn.setMinimumHeight(28)
            btn.setMinimumWidth(220)
            panel_layout.addWidget(btn)

        panel_layout.addWidget(QLabel("Bağlantı (Edge) İşlemleri"))
        self.edge_u_input = QLineEdit()
        self.edge_u_input.setPlaceholderText("Kaynak id (u)")
        self.edge_v_input = QLineEdit()
        self.edge_v_input.setPlaceholderText("Hedef id (v)")
        edge_inputs = [self.edge_u_input, self.edge_v_input]
        for w in edge_inputs:
            w.setMinimumHeight(26)
            w.setMinimumWidth(220)
            panel_layout.addWidget(w)

        btn_edge_add = QPushButton("Edge ekle")
        btn_edge_delete = QPushButton("Edge sil")
        btn_edge_add.clicked.connect(self.add_edge)
        btn_edge_delete.clicked.connect(self.delete_edge)
        edge_buttons = [btn_edge_add, btn_edge_delete]
        for btn in edge_buttons:
            btn.setMinimumHeight(28)
            btn.setMinimumWidth(220)
            panel_layout.addWidget(btn)

        btn_export_json = QPushButton("JSON dışa aktar")
        btn_export_csv = QPushButton("CSV dışa aktar")
        btn_adj_list = QPushButton("Komşuluk listesi CSV")
        btn_adj_matrix = QPushButton("Komşuluk matrisi CSV")
        btn_import_json = QPushButton("JSON içe aktar")
        btn_import_csv = QPushButton("CSV içe aktar")
        btn_reset = QPushButton("Başlangıç grafa dön")

        btn_export_json.clicked.connect(self.export_json)
        btn_export_csv.clicked.connect(self.export_csv)
        btn_adj_list.clicked.connect(self.export_adj_list)
        btn_adj_matrix.clicked.connect(self.export_adj_matrix)
        btn_import_json.clicked.connect(self.import_json)
        btn_import_csv.clicked.connect(self.import_csv)
        btn_reset.clicked.connect(self.reset_graph)

        panel_layout.addWidget(QLabel("Veri içe/dışa aktarım"))
        io_buttons = [
            btn_export_json,
            btn_export_csv,
            btn_adj_list,
            btn_adj_matrix,
            btn_import_json,
            btn_import_csv,
            btn_reset,
        ]
        for btn in io_buttons:
            btn.setMinimumHeight(30)
            btn.setMinimumWidth(220)
            panel_layout.addWidget(btn)

        panel_layout.addStretch()

        splitter.addWidget(panel)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setMinimumHeight(200)
        self.result.setStyleSheet(
            """
            QTextEdit {
                background-color: #1f1f1f;
                border: 2px solid #444444;
                border-radius: 4px;
                padding: 8px;
                color: #f0f0f0;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
            }
        """
        )

        main_layout.addWidget(splitter, stretch=3)
        main_layout.addWidget(QLabel("Sonuçlar"), stretch=0)
        main_layout.addWidget(self.result, stretch=1)

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
        if hasattr(self.canvas, "_calculate_layout"):
            self.canvas._calculate_layout()
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
        color_map = {}
        for idx, node_id in enumerate(visited):
            color_map[node_id] = idx % 9
        self.canvas.set_colors(color_map)
        self.canvas.set_path(visited)
        lines = ["BFS Gezinti Sırası:"]
        for i, node_id in enumerate(visited):
            lines.append(f"{i+1}. Node {node_id}")
        lines.append(f"\nToplam {len(visited)} node ziyaret edildi.")
        lines.append(f"Süre: {elapsed:.2f} ms")
        self._set_result("\n".join(lines))

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
        color_map = {}
        for idx, node_id in enumerate(visited):
            color_map[node_id] = idx % 9
        self.canvas.set_colors(color_map)
        self.canvas.set_path(visited)
        lines = ["DFS Gezinti Sırası:"]
        for i, node_id in enumerate(visited):
            lines.append(f"{i+1}. Node {node_id}")
        lines.append(f"\nToplam {len(visited)} node ziyaret edildi.")
        lines.append(f"Süre: {elapsed:.2f} ms")
        self._set_result("\n".join(lines))

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
        lines = ["En Etkili 5 Kullanıcı (Derece Merkezilik):"]
        lines.append("=" * 50)
        lines.append(f"{'Sıra':<6} {'ID':<6} {'İsim':<20} {'Derece':<8}")
        lines.append("-" * 50)
        for idx, (nid, deg) in enumerate(centrality, 1):
            node = self.graph.nodes.get(nid)
            node_name = node.name if node else f"Node{nid}"
            lines.append(f"{idx:<6} {nid:<6} {node_name:<20} {deg:<8}")
        lines.append("=" * 50)
        lines.append(f"\nSüre: {elapsed:.2f} ms")
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
        path, _ = QFileDialog.getSaveFileName(
            self,
            "JSON Olarak Kaydet",
            os.path.join(self.data_dir, "graph_export.json"),
            "JSON Files (*.json);;All Files (*)"
        )
        if not path:
            return
        try:
            Exporter.export_graph_json(self.graph, path)
            self._set_result(f"JSON kaydedildi: {path}")
            QMessageBox.information(self, "Başarılı", f"Graf başarıyla kaydedildi:\n{path}")
        except Exception as e:
            self._set_result(f"JSON kaydedilemedi: {e}")
            QMessageBox.critical(self, "Hata", f"Graf kaydedilemedi:\n{e}")

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "CSV Olarak Kaydet",
            os.path.join(self.data_dir, "graph_export.csv"),
            "CSV Files (*.csv);;All Files (*)"
        )
        if not path:
            return
        try:
            Exporter.export_graph_csv(self.graph, path)
            self._set_result(f"CSV kaydedildi: {path}")
            QMessageBox.information(self, "Başarılı", f"Graf başarıyla kaydedildi:\n{path}")
        except Exception as e:
            self._set_result(f"CSV kaydedilemedi: {e}")
            QMessageBox.critical(self, "Hata", f"Graf kaydedilemedi:\n{e}")

    def export_adj_list(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Komşuluk Listesi Olarak Kaydet",
            os.path.join(self.data_dir, "adjacency_list.csv"),
            "CSV Files (*.csv);;All Files (*)"
        )
        if not path:
            return
        try:
            Exporter.export_adjacency_list(self.graph, path)
            self._set_result(f"Komşuluk listesi kaydedildi: {path}")
            QMessageBox.information(self, "Başarılı", f"Komşuluk listesi kaydedildi:\n{path}")
        except Exception as e:
            self._set_result(f"Komşuluk listesi kaydedilemedi: {e}")
            QMessageBox.critical(self, "Hata", f"Komşuluk listesi kaydedilemedi:\n{e}")

    def export_adj_matrix(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Komşuluk Matrisi Olarak Kaydet",
            os.path.join(self.data_dir, "adjacency_matrix.csv"),
            "CSV Files (*.csv);;All Files (*)"
        )
        if not path:
            return
        try:
            Exporter.export_adjacency_matrix(self.graph, path)
            self._set_result(f"Komşuluk matrisi kaydedildi: {path}")
            QMessageBox.information(self, "Başarılı", f"Komşuluk matrisi kaydedildi:\n{path}")
        except Exception as e:
            self._set_result(f"Komşuluk matrisi kaydedilemedi: {e}")
            QMessageBox.critical(self, "Hata", f"Komşuluk matrisi kaydedilemedi:\n{e}")

    def import_json(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "JSON Dosyası Seç",
            self.data_dir,
            "JSON Files (*.json);;All Files (*)"
        )
        if not path:
            return
        try:
            g = Loader.load_graph_from_json(path)
            self.graph = g
            self._refresh_canvas()
            self._set_result(f"JSON'dan grafik yüklendi: {path}")
            QMessageBox.information(self, "Başarılı", f"Graf başarıyla yüklendi:\n{path}")
        except Exception as e:
            self._set_result(f"JSON içe aktarılamadı: {e}")
            QMessageBox.critical(self, "Hata", f"Graf yüklenemedi:\n{e}")

    def import_csv(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "CSV Dosyası Seç",
            self.data_dir,
            "CSV Files (*.csv);;All Files (*)"
        )
        if not path:
            return
        try:
            g = Loader.load_graph_from_csv(path)
            self.graph = g
            self._refresh_canvas()
            self._set_result(f"CSV'den grafik yüklendi: {path}")
            QMessageBox.information(self, "Başarılı", f"Graf başarıyla yüklendi:\n{path}")
        except Exception as e:
            self._set_result(f"CSV içe aktarılamadı: {e}")
            QMessageBox.critical(self, "Hata", f"Graf yüklenemedi:\n{e}")

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
