# ui/canvas.py
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QFontMetrics
from PyQt5.QtCore import Qt

class Canvas(QWidget):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.radius = 40

        self.positions = {}        # nodeId -> (x,y)
        self.selected_nodes = []   # tıklanan node id'leri (max 2)
        self.path_nodes = set()    # en kısa yol üzerindeki node'lar
        self.path_edges = set()    # en kısa yol üzerindeki kenarlar (u,v)

    def set_path(self, path):
        """Dijkstra sonucu gelen path'i kaydet ve yeniden çiz."""
        self.path_nodes = set(path)
        self.path_edges = set()
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            # hem (u,v) hem (v,u) kontrolü için normalize et
            self.path_edges.add(tuple(sorted((u, v))))
        self.update()

    def clear_path(self):
        self.path_nodes.clear()
        self.path_edges.clear()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(self.rect(), QColor(0, 0, 0))

        # --- POZİSYONLAR ---
        self.positions.clear()
        i = 0
        for node in self.graph.nodes.values():
            x = 150 + i * 140
            y = 180 + (i % 2) * 80
            self.positions[node.id] = (x, y)
            i += 1

        # --- EDGELER ---
        edge_pen = QPen(QColor(255, 255, 255))
        edge_pen.setWidth(2)
        painter.setPen(edge_pen)

        for (u, v), edge in self.graph.edges.items():
            key = tuple(sorted((u, v)))
            if key in self.path_edges:
                # path üzerindeki kenar → kalın ve farklı renk
                path_pen = QPen(QColor(0, 200, 255))
                path_pen.setWidth(4)
                painter.setPen(path_pen)
            else:
                painter.setPen(edge_pen)

            if u not in self.positions or v not in self.positions:
                continue

            x1, y1 = self.positions[u]
            x2, y2 = self.positions[v]

            dx = x2 - x1
            dy = y2 - y1
            length = (dx ** 2 + dy ** 2) ** 0.5 or 1
            ux = dx / length
            uy = dy / length
            r = self.radius

            sx = x1 + ux * r
            sy = y1 + uy * r
            ex = x2 - ux * r
            ey = y2 - uy * r

            painter.drawLine(int(sx), int(sy), int(ex), int(ey))

        # --- NODE’LAR ---
        font = QFont("Arial", 10)
        painter.setFont(font)
        fm = QFontMetrics(font)

        base_pen = QPen(QColor(255, 255, 255))
        base_pen.setWidth(2)

        for node in self.graph.nodes.values():
            x, y = self.positions[node.id]
            r = self.radius

            # renkler:
            if node.id in self.path_nodes:
                brush_color = QColor(0, 200, 255)   # path üzerindekiler dolu turkuaz
                text_color = QColor(0, 0, 0)
            elif node.id in self.selected_nodes:
                brush_color = QColor(0, 255, 0)     # seçilmiş start/end → yeşil
                text_color = QColor(0, 0, 0)
            else:
                brush_color = QColor(0, 0, 0)
                text_color = QColor(255, 255, 255)

            painter.setPen(base_pen)
            painter.setBrush(brush_color)
            painter.drawEllipse(int(x - r), int(y - r), int(2 * r), int(2 * r))

            text = f"{node.name} ({node.id})"
            tw = fm.horizontalAdvance(text)
            th = fm.height()
            tx = x - tw / 2
            ty = y + th / 4

            painter.setPen(text_color)
            painter.drawText(int(tx), int(ty), text)

    # --- NODE TIKLAMA ---

    def mousePressEvent(self, event):
        pos = event.pos()
        clicked_id = None

        for node_id, (x, y) in self.positions.items():
            dx = pos.x() - x
            dy = pos.y() - y
            if (dx*dx + dy*dy) ** 0.5 <= self.radius:
                clicked_id = node_id
                break

        if clicked_id is not None:
            if clicked_id in self.selected_nodes:
                # tekrar tıklarsa seçimden çıkar
                self.selected_nodes.remove(clicked_id)
            else:
                if len(self.selected_nodes) >= 2:
                    self.selected_nodes = []
                self.selected_nodes.append(clicked_id)

            # yeni seçimde eski path’i silelim
            self.clear_path()
            self.update()
