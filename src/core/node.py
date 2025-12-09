class Node:
    def __init__(self, id, name="", aktiflik=0, etkilesim=0, baglanti_sayisi=0):
        self.id = id
        self.name = name
        self.aktiflik = aktiflik
        self.etkilesim = etkilesim
        self.baglanti_sayisi = baglanti_sayisi
        self.neighbors = []  # komşu id listesi

    def add_neighbor(self, neighbor_id):
        if neighbor_id not in self.neighbors:
            self.neighbors.append(neighbor_id)

    def __repr__(self):
        return f"Node({self.id}, {self.name})"
