from queue import PriorityQueue
import math


class Algorithm:
    def __init__(self, name: str):
        self.name = name
        self.duration_ms = 0.0
        self.result = None

    def run(self, graph, **kwargs):
        raise NotImplementedError


class Coloring:
    def __init__(self, color_map=None):
        self.color_map = color_map or {}


class Algorithms:
    @staticmethod
    def bfs(graph, start):
        visited = []
        queue = [start]

        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.append(node)
                queue.extend(graph.nodes[node].neighbors)

        return visited

    @staticmethod
    def dfs(graph, start, visited=None):
        if visited is None:
            visited = []

        visited.append(start)
        for neighbor in graph.nodes[start].neighbors:
            if neighbor not in visited:
                Algorithms.dfs(graph, neighbor, visited)
        return visited

    @staticmethod
    def dijkstra(graph, start_id, end_id):
        if start_id not in graph.nodes or end_id not in graph.nodes:
            return [], float("inf")

        dist = {nid: float("inf") for nid in graph.nodes}
        prev = {}

        dist[start_id] = 0
        pq = PriorityQueue()
        pq.put((0, start_id))

        while not pq.empty():
            curr_dist, u = pq.get()

            if curr_dist > dist[u]:
                continue

            if u == end_id:
                break

            for v in graph.nodes[u].neighbors:
                weight = graph.edges[(u, v)].weight
                new_dist = curr_dist + weight

                if new_dist < dist[v]:
                    dist[v] = new_dist
                    prev[v] = u
                    pq.put((new_dist, v))

        if end_id not in prev and start_id != end_id:
            return [], float("inf")

        path = [end_id]
        while path[-1] != start_id:
            path.append(prev[path[-1]])
        path.reverse()

        return path, dist[end_id]

    @staticmethod
    def a_star(graph, start_id, end_id):
        if start_id not in graph.nodes or end_id not in graph.nodes:
            return [], float("inf")

        def heuristic(u, v):
            n1, n2 = graph.nodes[u], graph.nodes[v]
            d1 = (n1.aktiflik - n2.aktiflik) ** 2
            d2 = (n1.etkilesim - n2.etkilesim) ** 2
            d3 = (n1.baglanti_sayisi - n2.baglanti_sayisi) ** 2
            return math.sqrt(d1 + d2 + d3)

        open_set = PriorityQueue()
        open_set.put((0, start_id))

        g_score = {nid: float("inf") for nid in graph.nodes}
        f_score = {nid: float("inf") for nid in graph.nodes}
        came_from = {}

        g_score[start_id] = 0
        f_score[start_id] = heuristic(start_id, end_id)

        visited = set()

        while not open_set.empty():
            _, current = open_set.get()
            if current in visited:
                continue
            visited.add(current)

            if current == end_id:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path, g_score[end_id]

            for neighbor in graph.nodes[current].neighbors:
                weight = graph.edges[(current, neighbor)].weight
                tentative_g = g_score[current] + weight

                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, end_id)
                    open_set.put((f_score[neighbor], neighbor))

        return [], float("inf")

    @staticmethod
    def connected_components(graph):
        visited = set()
        components = []

        for nid in graph.nodes:
            if nid in visited:
                continue
            comp = []
            stack = [nid]
            while stack:
                u = stack.pop()
                if u in visited:
                    continue
                visited.add(u)
                comp.append(u)
                for v in graph.nodes[u].neighbors:
                    if v not in visited:
                        stack.append(v)
            components.append(comp)
        return components

    @staticmethod
    def degree_centrality(graph, top_n=5):
        degrees = []
        for nid, node in graph.nodes.items():
            degrees.append((nid, len(node.neighbors)))
        degrees.sort(key=lambda x: x[1], reverse=True)
        return degrees[:top_n]

    @staticmethod
    def welsh_powell(graph):
        order = sorted(graph.nodes.keys(), key=lambda nid: len(graph.nodes[nid].neighbors), reverse=True)
        color_assignment = {}
        current_color = 0

        for nid in order:
            if nid in color_assignment:
                continue
            color_assignment[nid] = current_color
            for other in order:
                if other in color_assignment:
                    continue
                if all(color_assignment.get(nei) != current_color for nei in graph.nodes[other].neighbors):
                    color_assignment[other] = current_color
            current_color += 1

        return color_assignment