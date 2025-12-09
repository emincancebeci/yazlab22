from queue import PriorityQueue

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
    def dijkstra(graph, start, end):
        dist = {n: float('inf') for n in graph.nodes}
        dist[start] = 0
        pq = PriorityQueue()
        pq.put((0, start))
        prev = {}

        while not pq.empty():
            curr_dist, u = pq.get()

            if u == end:
                break

            for v in graph.nodes[u].neighbors:
                weight = graph.edges[(u, v)].weight
                new_dist = curr_dist + weight

                if new_dist < dist[v]:
                    dist[v] = new_dist
                    prev[v] = u
                    pq.put((new_dist, v))

        # PATH ÇIKAR
        path = []
        curr = end
        while curr in prev:
            path.append(curr)
            curr = prev[curr]
        path.append(start)
        path.reverse()

        return path, dist[end]
