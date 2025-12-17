import sys
import os
from PyQt5.QtWidgets import QApplication

sys.path.append(os.path.dirname(__file__))

from ui.app import App
from io_.loader import Loader


def main():
   
    base_dir = os.path.dirname(os.path.abspath(__file__))

    
    graph_path = os.path.join(base_dir, "data", "graph.json")

    try:
        graph = Loader.load_graph_from_json(graph_path)
        print("[INFO] Graph successfully loaded from:", graph_path)
    except Exception as e:
        print("[ERROR] Graph yüklenemedi:", e)
        return

    app = QApplication(sys.argv)
    # Başlangıç grafı path'ini App'e ilet ki reset butonu çalışsın
    window = App(graph, initial_graph_path=graph_path)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
