import os
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
from io_.exporter import Exporter
from .canvas import Canvas


class App(QMainWindow):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.setWindowTitle("Sosyal Ağ Analizi")
        self.resize(1200, 700)

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Sol: Canvas
        self.canvas = Canvas(graph)
        main_layout.addWidget(self.canvas, stretch=3)

        # Sağ: Kontrol paneli
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

        # Export butonları
        btn_export_json = QPushButton("JSON dışa aktar")
        btn_export_csv = QPushButton("CSV dışa aktar")
        btn_adj_list = QPushButton("Komşuluk listesi CSV")
        btn_adj_matrix = QPushButton("Komşuluk matrisi CSV")
        btn_export_json.clicked.connect(self.export_json)
        btn_export_csv.clicked.connect(self.export_csv)
        btn_adj_list.clicked.connect(self.export_adj_list)
        btn_adj_matrix.clicked.connect(self.export_adj_matrix)
        panel_layout.addWidget(QLabel("Dışa aktarım"))
        for btn in [btn_export_json, btn_export_csv, btn_adj_list, btn_adj_matrix]:
            panel_layout.addWidget(btn)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        panel_layout.addWidget(QLabel("Sonuç"))
        panel_layout.addWidget(self.result)
        panel_layout.addStretch()

        main_layout.addWidget(panel, stretch=1)
        self.setCentralWidget(main_widget)

        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.data_dir = os.path.join(self.base_dir, "data")
        os.makedirs(self.data_dir, exist_ok=True)

    # --- Yardımcılar ---
    def _parse_int(self, text):
        try:
            return int(text)
        except Exception:
            return None

    def _set_result(self, message):
        self.result.setPlainText(message)

    # --- Algoritmalar ---
    def run_bfs(self):
        start = self._parse_int(self.start_input.text())
        if start is None or start not in self.graph.nodes:
            self._set_result("Geçerli bir başlangıç id gir.")
            return
        self.canvas.clear_path()
        visited = Algorithms.bfs(self.graph, start)
        self._set_result(f"BFS sırası: {visited}")

    def run_dfs(self):
        start = self._parse_int(self.start_input.text())
        if start is None or start not in self.graph.nodes:
            self._set_result("Geçerli bir başlangıç id gir.")
            return
        self.canvas.clear_path()
        visited = Algorithms.dfs(self.graph, start, [])
        self._set_result(f"DFS sırası: {visited}")

    def run_dijkstra(self):
        start = self._parse_int(self.start_input.text())
        end = self._parse_int(self.end_input.text())
        if start is None or end is None:
            self._set_result("Başlangıç ve bitiş id gir.")
            return
        path, dist = Algorithms.dijkstra(self.graph, start, end)
        if not path:
            self.canvas.clear_path()
            self._set_result("Yol bulunamadı.")
            return
        self.canvas.set_path(path)
        self._set_result(f"Dijkstra yol: {path} | Maliyet: {dist:.4f}")

    def run_astar(self):
        start = self._parse_int(self.start_input.text())
        end = self._parse_int(self.end_input.text())
        if start is None or end is None:
            self._set_result("Başlangıç ve bitiş id gir.")
            return
        path, dist = Algorithms.a_star(self.graph, start, end)
        if not path:
            self.canvas.clear_path()
            self._set_result("Yol bulunamadı.")
            return
        self.canvas.set_path(path)
        self._set_result(f"A* yol: {path} | Maliyet: {dist:.4f}")

    def run_components(self):
        comps = Algorithms.connected_components(self.graph)
        self.canvas.clear_path()
        self.canvas.set_colors({})
        formatted = "\n".join([f"{i+1}. bileşen: {c}" for i, c in enumerate(comps)])
        self._set_result(formatted)

    def run_degree(self):
        centrality = Algorithms.degree_centrality(self.graph, top_n=5)
        lines = [f"{nid} -> derece {deg}" for nid, deg in centrality]
        self.canvas.clear_path()
        self._set_result("\n".join(lines))

    def run_welsh(self):
        colors = Algorithms.welsh_powell(self.graph)
        self.canvas.clear_path()
        self.canvas.set_colors(colors)
        lines = [f"Node {nid} -> Renk {color}" for nid, color in colors.items()]
        self._set_result("\n".join(lines))

    # --- Export işlemleri ---
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
