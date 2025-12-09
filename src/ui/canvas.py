from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QFontMetrics
from PyQt5.QtCore import Qt

class Canvas(QWidget):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.radius = 35  

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(self.rect(), QColor(0, 0, 0))

       
        positions = {}
        i = 0
        for node in self.graph.nodes.values():
          
            x = 120 + i * 120
            y = 150 + (i % 2) * 80
            positions[node.id] = (x, y)
            i += 1

    
        edge_pen = QPen(QColor(255, 255, 255))
        edge_pen.setWidth(2)
        painter.setPen(edge_pen)

        for (u, v), edge in self.graph.edges.items():
          
            if (v, u) in self.graph.edges and u > v:
                continue

            if u not in positions or v not in positions:
                continue

            x1, y1 = positions[u]
            x2, y2 = positions[v]

            dx = x2 - x1
            dy = y2 - y1
            length = (dx ** 2 + dy ** 2) ** 0.5 or 1

          
            ux = dx / length
            uy = dy / length

            r = self.radius

           
            start_x = x1 + ux * r
            start_y = y1 + uy * r
            end_x = x2 - ux * r
            end_y = y2 - uy * r

            painter.drawLine(int(start_x), int(start_y), int(end_x), int(end_y))

        
        node_pen = QPen(QColor(255, 255, 255))
        node_pen.setWidth(2)
        painter.setPen(node_pen)
        painter.setBrush(QColor(0, 0, 0))

        font = QFont("Arial", 10)
        painter.setFont(font)
        fm = QFontMetrics(font)
        r = self.radius

        for node in self.graph.nodes.values():
            x, y = positions[node.id]

        
            painter.drawEllipse(int(x - r), int(y - r), int(2 * r), int(2 * r))

           
            text = f"{node.name} ({node.id})"

            text_width = fm.horizontalAdvance(text)
            text_height = fm.height()

            text_x = x - text_width / 2
           
            text_y = y + text_height / 4

            painter.drawText(int(text_x), int(text_y), text)
