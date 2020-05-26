from os import path
from datetime import datetime
from enum import Enum, auto
from abc import ABC, abstractmethod
import networkx as nx

import logger as lg

DEFAULT_EXPORT_DIR = 'dot_output'
EXPORT_FILE_FORMAT = '%Y-%m-%d-%H-%M-%S-output.dot'
logger = lg.get_logger('HEL')


class HeuristicBase(ABC):

    STRING_BOOLEAN_REPRESENTATIONS = {
        'true': ['true', 'True', 'TRUE', 'T'],
        'false': ['false', 'False', 'FALSE', 'F']
    }
    DEFAULT_NO_STATEMENT_STRING = 'no valuable statements have been deduced'

    class TrivialDomain(Enum):
        NULLABLE = auto()
        BOOLEAN = auto()
        REAL = auto()
        INTEGER = auto()
        STRING = auto()

    @staticmethod
    def _is_bool_convertable_string(value):
        return (value in HeuristicBase.STRING_BOOLEAN_REPRESENTATIONS['true'] or
                value in HeuristicBase.STRING_BOOLEAN_REPRESENTATIONS['false'])

    @staticmethod
    def _is_int_convertable_string(value):
        result = True
        try:
            _ = int(value)
        except ValueError:
            result = False
        finally: 
            return result

    @staticmethod
    def _is_float_convertable_string(value):
        result = True
        try:
            _ = float(value)
        except ValueError:
            result = False
        finally: 
            return result

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

    @staticmethod
    def test_networkx():
        G = nx.MultiDiGraph()
        edges = [
            [1, 2, {'label': 'foo'}],
            [1, 3, {'label': 'bar'}],
            [2, 4, {'label': 'baz'}],
            [3, 4, {'label': 'qux'}],
        ]
        G.add_edges_from(edges)
        HeuristicBase.export_graph_to_dot(G)

    # log_data is not empty, which should be controlled before object instantiation
    def __init__(self, log_data: list):
        self.log_data = log_data
        self.attr_names = list(log_data[0].keys())

    def deduce_attribute_type(self, attr_name):
        # Map for possible types conversions which is to cast values to ones
        # of more appropriate type, i.e. "true" [str] -> True [Boolean];
        # key: message index,
        # value: proposed item value.
        suggested_clarifications = dict()
        values = [x[attr_name] for x in self.log_data]
        current_type = self.TrivialDomain.NULLABLE
        logger.info(f'deducing trivial type for {attr_name}...')
        for index, elem in enumerate(values):

            if not elem:
                continue

            if isinstance(elem, float):
                # to meet type consistency, attribute won't be mapped to any 
                # certain type if it comprise diverse values => leave NULLABLE
                if (current_type == self.TrivialDomain.BOOLEAN or
                    current_type == self.TrivialDomain.STRING):

                    current_type = self.TrivialDomain.NULLABLE
                    break;
                current_type = self.TrivialDomain.REAL

            elif isinstance(elem, int):
                if current_type != self.TrivialDomain.REAL:
                    if (current_type == self.TrivialDomain.BOOLEAN or
                        current_type == self.TrivialDomain.STRING):

                        current_type = self.TrivialDomain.NULLABLE
                        break;
                    current_type = self.TrivialDomain.INTEGER
                else:
                    suggested_clarifications[index] = float(elem)

            elif isinstance(elem, bool):
                if (current_type != self.TrivialDomain.NULLABLE and
                    current_type != self.TrivialDomain.BOOLEAN):

                        current_type = self.TrivialDomain.NULLABLE
                        break;
                current_type = self.TrivialDomain.BOOLEAN

            elif isinstance(elem, str):
                if current_type == self.TrivialDomain.BOOLEAN:
                    if self._is_bool_convertable_string(elem):
                        suggested_clarifications[index] = True \
                            if elem in self.STRING_BOOLEAN_REPRESENTATIONS['true'] \
                            else False
                    else:
                        current_type = self.TrivialDomain.NULLABLE
                        suggested_clarifications.clear()
                        break;

                elif current_type == self.TrivialDomain.INTEGER:
                    if self._is_int_convertable_string(elem):
                        suggested_clarifications[index] = int(elem)
                    elif self._is_float_convertable_string(elem):
                        current_type = self.TrivialDomain.REAL
                        suggested_clarifications = float(elem)
                    else:
                        current_type = self.TrivialDomain.STRING
                        suggested_clarifications = \
                            {x: str(suggested_clarifications[x]) for x 
                             in suggested_clarifications}

                elif current_type == self.TrivialDomain.REAL:
                    if self._is_float_convertable_string(elem):
                        suggested_clarifications = float(elem)
                    else:
                        current_type = self.TrivialDomain.STRING
                        suggested_clarifications = \
                            [{x: str(suggested_clarifications[x])} for x 
                             in suggested_clarifications]

                elif current_type == self.TrivialDomain.NULLABLE:
                    if self._is_bool_convertable_string(elem):
                        suggested_clarifications[index] = True \
                            if elem in self.STRING_BOOLEAN_REPRESENTATIONS['true'] \
                            else False
                    elif self._is_int_convertable_string(elem):
                        current_type = self.TrivialDomain.INTEGER
                        suggested_clarifications[index] = int(elem)
                    elif self._is_float_convertable_string(elem):
                        current_type = self.TrivialDomain.REAL
                        suggested_clarifications[index] = float(elem)
                    else:
                        current_type = self.TrivialDomain.STRING

        logger.info(f'inferred trivial type as {current_type}')
        return {
            'type_assignment': current_type,
            'suggested_clarifications': suggested_clarifications,
        }

    @abstractmethod
    def infer_statement_for_integer(self, values):
        raise NotImplementedError

    @abstractmethod
    def infer_statement_for_float(self, values):
        raise NotImplementedError

    @abstractmethod
    def infer_statement_for_boolean(self, values):
        raise NotImplementedError

    @abstractmethod
    def infer_statement_for_string(self, values):
        raise NotImplementedError

    def get_global_attribute_statement(self, attr_name):

        deduce_result = self.deduce_attribute_type(attr_name)
        # `refined_values` is a list of values for `attr_name` intended to be 
        # repaired on suggested clarifications
        refined_values = [x[attr_name] for x in self.log_data]
        clarifications = deduce_result['suggested_clarifications']
        type_assignment = deduce_result['type_assignment']
        for index in clarifications:
            refined_values[index] = clarifications[index]

        statement = f'base type: {type_assignment.name}'
        if type_assignment == self.TrivialDomain.INTEGER:
            statement = '; '.join([
                statement, 
                self.infer_statement_for_integer(refined_values)
            ])
        elif type_assignment == self.TrivialDomain.REAL:
            statement = '; '.join([
                statement, 
                self.infer_statement_for_float(refined_values)
            ])
        elif type_assignment == self.TrivialDomain.BOOLEAN:
            statement = '; '.join([
                statement, 
                self.infer_statement_for_boolean(refined_values)
            ])
        elif type_assignment == self.TrivialDomain.STRING:
            statement = '; '.join([
                statement, 
                self.infer_statement_for_string(refined_values)
            ])
        else:
            statement = '; '.join([
                statement, 
                'no meaningful assessment for type-inconsistent data'
            ])

        return statement if statement else self.DEFAULT_NO_STATEMENT_STRING

    @abstractmethod
    def process_messages(self, data: dict):
        """
        The most general method for particular heuristic. Commonly, it appears 
        as an entrance point for analysis. Meant to be a caller for the rest of 
        methods.
        """
        raise NotImplementedError


if __name__ == '__main__':
    logger.info('running test method...')
    HeuristicBase.test_networkx()
