from PyQt5.QtWidgets import QApplication, QMainWindow
from .canvas import Canvas

class App(QMainWindow):
    def __init__(self, graph):
        super().__init__()

        self.setWindowTitle("Sosyal Ağ Analizi")
        self.canvas = Canvas(graph)
        self.setCentralWidget(self.canvas)
