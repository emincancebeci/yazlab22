from queue import PriorityQueue


class Algorithm:
    """Genel algoritma arayüzü (raporlama / genişletme için)."""

    def __init__(self, name: str):
        self.name = name
        self.duration_ms = 0.0
        self.result = None

    def run(self, graph, **kwargs):
        raise NotImplementedError("run metodu alt sınıflarda uygulanmalıdır.")


class Coloring:
    """Düğümler için renk atamalarını temsil eder."""

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
        # başlangıç kontrolü
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

        # yol çıkar
        if end_id not in prev and start_id != end_id:
            return [], float("inf")

        path = [end_id]
        while path[-1] != start_id:
            path.append(prev[path[-1]])
        path.reverse()

        return path, dist[end_id]