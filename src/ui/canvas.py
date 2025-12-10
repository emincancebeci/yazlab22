from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QFontMetrics
from PyQt5.QtCore import Qt


class Canvas(QWidget):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.radius = 35
        self.positions = {}
        self.path_nodes = set()
        self.path_edges = set()
        self.node_colors = {}
        # basit renk paleti
        self.palette = [
            QColor("#00bcd4"), QColor("#8bc34a"), QColor("#ffc107"),
            QColor("#e91e63"), QColor("#9c27b0"), QColor("#3f51b5"),
            QColor("#ff5722"), QColor("#009688"), QColor("#607d8b")
        ]

    # --- DIŞ ARAYÜZ ---
    def set_path(self, path):
        self.path_nodes = set(path)
        self.path_edges = set()
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            self.path_edges.add(tuple(sorted((u, v))))
        self.update()

    def clear_path(self):
        self.path_nodes.clear()
        self.path_edges.clear()
        self.update()

    def set_colors(self, color_map):
        self.node_colors = color_map or {}
        self.update()

    # --- ÇİZİM ---
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(0, 0, 0))

        # yerleşim
        self.positions.clear()
        i = 0
        for node in self.graph.nodes.values():
            x = 120 + i * 120
            y = 150 + (i % 2) * 80
            self.positions[node.id] = (x, y)
            i += 1

        # kenarlar
        base_edge_pen = QPen(QColor(255, 255, 255))
        base_edge_pen.setWidth(2)

        path_edge_pen = QPen(QColor("#00bcd4"))
        path_edge_pen.setWidth(4)

        for (u, v), edge in self.graph.edges.items():
            if (v, u) in self.graph.edges and u > v:
                continue
            if u not in self.positions or v not in self.positions:
                continue

            key = tuple(sorted((u, v)))
            painter.setPen(path_edge_pen if key in self.path_edges else base_edge_pen)

            x1, y1 = self.positions[u]
            x2, y2 = self.positions[v]
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

        # düğümler
        font = QFont("Arial", 10)
        painter.setFont(font)
        fm = QFontMetrics(font)
        r = self.radius

        for node in self.graph.nodes.values():
            x, y = self.positions[node.id]
            # renk seçimi
            if node.id in self.node_colors:
                color_idx = self.node_colors[node.id] % len(self.palette)
                fill_color = self.palette[color_idx]
                text_color = QColor(0, 0, 0)
            elif node.id in self.path_nodes:
                fill_color = QColor("#00bcd4")
                text_color = QColor(0, 0, 0)
            else:
                fill_color = QColor(0, 0, 0)
                text_color = QColor(255, 255, 255)

            pen = QPen(QColor(255, 255, 255))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(fill_color)
            painter.drawEllipse(int(x - r), int(y - r), int(2 * r), int(2 * r))

            text = f"{node.name} ({node.id})"
            tw = fm.horizontalAdvance(text)
            th = fm.height()
            painter.setPen(text_color)
            painter.drawText(int(x - tw / 2), int(y + th / 4), text)
