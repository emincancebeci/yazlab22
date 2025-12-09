# ui/app.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from .canvas import Canvas
from core.algorithms import Algorithms

class App(QMainWindow):
    def __init__(self, graph):
        super().__init__()

        self.graph = graph
        self.setWindowTitle("Sosyal Ağ Analizi")
        self.resize(1000, 600)

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # SOL: Canvas
        self.canvas = Canvas(self.graph)
        main_layout.addWidget(self.canvas, stretch=3)

        # SAĞ: Kontrol paneli
        side_panel = QWidget()
        side_layout = QVBoxLayout(side_panel)

        self.info_label = QLabel("Başlangıç ve bitiş node'unu seçmek için node'lara tıkla.")
        self.result_label = QLabel("Seçili: -")
        self.info_label.setStyleSheet("color: white;")
        self.result_label.setStyleSheet("color: white;")

        btn_dijkstra = QPushButton("En Kısa Yol (Dijkstra)")
        btn_dijkstra.clicked.connect(self.run_dijkstra)

        side_layout.addWidget(self.info_label)
        side_layout.addWidget(self.result_label)
        side_layout.addWidget(btn_dijkstra)
        side_layout.addStretch()

        side_panel.setStyleSheet("background-color: #111111; color: white;")

        main_layout.addWidget(side_panel, stretch=1)

        self.setCentralWidget(main_widget)

    def run_dijkstra(self):
        selected = self.canvas.selected_nodes
        if len(selected) != 2:
            self.result_label.setText("Lütfen 2 node seç (başlangıç ve bitiş).")
            return

        start, end = selected
        path, dist = Algorithms.dijkstra(self.graph, start, end)

        if not path:
            self.result_label.setText("Yol bulunamadı.")
            self.canvas.clear_path()
            return

        self.canvas.set_path(path)
        self.result_label.setText(
            f"En kısa yol: {' -> '.join(map(str, path))} | Maliyet: {dist:.4f}"
        )
