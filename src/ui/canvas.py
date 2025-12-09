from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor

class Canvas(QWidget):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph

    def paintEvent(self, event):
        painter = QPainter(self)

        pen = QPen(QColor(255,255,255))
        pen.setWidth(2)
        painter.setPen(pen)

        # basic node draw
        for node in self.graph.nodes.values():
            x = node.id * 50 + 50
            y = node.id * 30 + 50
            painter.drawEllipse(x, y, 20, 20)

        # edges
        for (u, v), edge in self.graph.edges.items():
            pu = self.graph.nodes[u].id * 50 + 60
            pv = self.graph.nodes[v].id * 50 + 60
            painter.drawLine(pu, pu, pv, pv)
