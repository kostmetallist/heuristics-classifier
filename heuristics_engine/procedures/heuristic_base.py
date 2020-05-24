from os import path
from datetime import datetime
from abc import ABC, abstractmethod
import networkx as nx

import logger as lg

DEFAULT_EXPORT_DIR = 'dot_output'
EXPORT_FILE_FORMAT = '%Y-%m-%d-%H-%M-%S-output.dot'
logger = lg.get_logger('HEL')


# class HeuristicBase(ABC):
class HeuristicBase:

    @abstractmethod
    def process_messages(self, data: dict):
        pass

    @staticmethod
    def export_graph_to_dot(graph, export_file_path=''):
        if not export_file_path:
            export_file = open(
                path.join(DEFAULT_EXPORT_DIR, 
                    datetime.now().strftime(EXPORT_FILE_FORMAT)), 
                mode='x', 
                encoding='UTF-8')
        else:
            export_file = open(export_file_path, 'x', encoding='UTF-8')

        logger.info(f'exporting graph to the {export_file.name}...')
        nx.drawing.nx_pydot.write_dot(graph, export_file)
        export_file.close()

    def test_networkx(self):
        G = nx.MultiDiGraph()
        edges = [
            [1, 2, {'label': 'foo'}],
            [1, 3, {'label': 'bar'}],
            [2, 4, {'label': 'baz'}],
            [3, 4, {'label': 'qux'}]]
        G.add_edges_from(edges)
        self.export_graph_to_dot(G)


if __name__ == '__main__':
    logger.info('running test method...')
    HeuristicBase().test_networkx()
