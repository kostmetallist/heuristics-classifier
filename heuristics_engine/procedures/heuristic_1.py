from procedures.heuristic_base import HeuristicBase


class Heuristic1(HeuristicBase):
    def process_messages(self, data: dict):
        pass


if __name__ == '__main__':
    h = Heuristic1()
    h.test_networkx()
