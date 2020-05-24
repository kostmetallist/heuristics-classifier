from abc import ABC, abstractmethod
import networkx as nx


# class HeuristicBase(ABC):
class HeuristicBase:

    @abstractmethod
    def process_messages(self, data: dict):
        pass

    @staticmethod
    def export_graph_to_dot(graph):
        pass

    def test_networkx(self):
        G = nx.Graph()
        G.add_edge(1, 2, weight=0.3)
        G.add_edge(1, 3, weight=0.5)
        G.add_edge(2, 4, weight=0.18)
        G.add_edge(3, 4, weight=0.02)


if __name__ == '__main__':
    hb = HeuristicBase()
    hb.test_networkx()
