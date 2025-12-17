from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QFontMetrics
from PyQt5.QtCore import Qt, QPoint


class Canvas(QWidget):
    def __init__(self, graph, node_click_callback=None):
        super().__init__()
        self.graph = graph
        self.radius = 35
        self.positions = {}
        self.selected_nodes = []
        self.path_nodes = set()
        self.path_edges = set()
        self.node_colors = {}
        self.node_click_callback = node_click_callback
        self.palette = [
            QColor("#00bcd4"),
            QColor("#8bc34a"),
            QColor("#ffc107"),
            QColor("#e91e63"),
            QColor("#9c27b0"),
            QColor("#3f51b5"),
            QColor("#ff5722"),
            QColor("#009688"),
            QColor("#607d8b"),
        ]
        self.setMinimumSize(800, 600)

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
        self._calculate_layout()
        self.update()

    def _detect_node_at(self, pos: QPoint):
        if not self.positions:
            return None
        x_click = pos.x()
        y_click = pos.y()
        r2 = self.radius * self.radius
        for nid, (x, y) in self.positions.items():
            dx = x_click - x
            dy = y_click - y
            if dx * dx + dy * dy <= r2:
                return nid
        return None

    def mousePressEvent(self, event):
        pos = event.pos()
        clicked_id = self._detect_node_at(pos)
        if clicked_id is None:
            return

        if clicked_id in self.selected_nodes:
            self.selected_nodes.remove(clicked_id)
        else:
            if len(self.selected_nodes) >= 2:
                self.selected_nodes = []
            self.selected_nodes.append(clicked_id)

        self.clear_path()
        if callable(self.node_click_callback):
            self.node_click_callback(clicked_id)
        self.update()

    def _calculate_layout(self):
        import math

        self.positions.clear()
        node_count = len(self.graph.nodes)
        if node_count == 0:
            return

        nodes = list(self.graph.nodes.values())
        center_x, center_y = 500, 500

        if node_count == 1:
            self.positions[nodes[0].id] = (center_x, center_y)
        elif node_count <= 4:
            radius = 150
            for i, node in enumerate(nodes):
                angle = 2 * math.pi * i / node_count - math.pi / 2
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                self.positions[node.id] = (x, y)
        elif node_count <= 12:
            radius = 200
            for i, node in enumerate(nodes):
                angle = 2 * math.pi * i / node_count - math.pi / 2
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                self.positions[node.id] = (x, y)
        else:
            layers = int(math.ceil(math.sqrt(node_count / 8))) + 1
            placed = 0
            layer = 0

            while placed < node_count:
                if layer == 0:
                    self.positions[nodes[placed].id] = (center_x, center_y)
                    placed += 1
                    layer += 1
                    continue

                nodes_in_layer = min(8 * layer, node_count - placed)
                if nodes_in_layer <= 0:
                    break

                radius = 120 + layer * 100
                for i in range(nodes_in_layer):
                    if placed >= node_count:
                        break
                    angle = 2 * math.pi * i / nodes_in_layer - math.pi / 2
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                    self.positions[nodes[placed].id] = (x, y)
                    placed += 1
                layer += 1

        if not self.positions:
            return

        max_x = max(pos[0] for pos in self.positions.values()) + self.radius * 2
        max_y = max(pos[1] for pos in self.positions.values()) + self.radius * 2
        min_x = min(pos[0] for pos in self.positions.values()) - self.radius * 2
        min_y = min(pos[1] for pos in self.positions.values()) - self.radius * 2

        width = max(1000, int(max_x - min_x + 300))
        height = max(800, int(max_y - min_y + 300))
        self.setMinimumSize(width, height)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(self.rect(), QColor("#121212"))

        if not self.positions:
            self._calculate_layout()

        base_edge_pen = QPen(QColor(180, 180, 180))
        base_edge_pen.setWidth(2)

        path_edge_pen = QPen(QColor(0, 200, 255))
        path_edge_pen.setWidth(4)

        drawn_edges = set()
        for (u, v), edge in self.graph.edges.items():
            key = tuple(sorted((u, v)))
            if u not in self.positions or v not in self.positions:
                continue
            if key in drawn_edges:
                continue
            drawn_edges.add(key)

            painter.setPen(path_edge_pen if key in self.path_edges else base_edge_pen)

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

            # Kenar ağırlığını çizginin hafif yanına yaz
            if len(self.graph.nodes) <= 20:
                mid_x = (sx + ex) / 2
                mid_y = (sy + ey) / 2

                offset = 14
                nx = -uy
                ny = ux
                label_x = mid_x + nx * offset
                label_y = mid_y + ny * offset

                weight_text = f"{edge.weight:.2f}"
                old_font = painter.font()
                weight_font = QFont(old_font)
                weight_font.setPointSize(max(8, old_font.pointSize() + 1))
                weight_font.setBold(True)
                painter.setFont(weight_font)

                painter.setPen(QColor(255, 255, 150))
                painter.drawText(int(label_x - 15), int(label_y), weight_text)
                painter.setFont(old_font)

        font = QFont("Segoe UI", 10)
        painter.setFont(font)
        fm = QFontMetrics(font)

        base_pen = QPen(QColor(230, 230, 230))
        base_pen.setWidth(2)

        for node in self.graph.nodes.values():
            x, y = self.positions[node.id]
            r = self.radius

            if node.id in self.node_colors:
                idx = self.node_colors[node.id] % len(self.palette)
                brush_color = self.palette[idx]
                text_color = QColor(0, 0, 0)
            elif node.id in self.path_nodes:
                brush_color = QColor(0, 200, 255)
                text_color = QColor(0, 0, 0)
            elif node.id in self.selected_nodes:
                brush_color = QColor(76, 175, 80)
                text_color = QColor(0, 0, 0)
            else:
                brush_color = QColor(30, 30, 30)
                text_color = QColor(240, 240, 240)

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
