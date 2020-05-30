from os import path
from datetime import datetime
from enum import Enum, auto
from abc import ABC, abstractmethod
from pprint import pformat
import networkx as nx

import logger as lg
from datastructures.referenced_sequence import ReferencedSequence
from datastructures.statement import Statement

DEFAULT_DOT_EXPORT_DIR = 'output/dot_output'
DOT_FILENAME_FORMAT = '%Y-%m-%d-%H-%M-%S-output.dot'
logger = lg.get_logger('HEL')


class HeuristicBase(ABC):

    STRING_BOOLEAN_REPRESENTATIONS = {
        'true': ['true', 'True', 'TRUE', 'T'],
        'false': ['false', 'False', 'FALSE', 'F']
    }

    INTEGER_CARDINALITY_LIMIT = 5
    STRING_CARDINALITY_LIMIT = 5
    STEREOTYPE_RATIO_THRESHOLD = .7

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
                path.join(DEFAULT_DOT_EXPORT_DIR, 
                    datetime.now().strftime(DOT_FILENAME_FORMAT)), 
                mode='x', 
                encoding='UTF-8')
        else:
            export_file = open(export_file_path, 'w', encoding='UTF-8')

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
        # of more appropriate type, i.e. "true" [str] -> True [bool];
        # key: message index,
        # value: proposed item value.
        suggested_clarifications = dict()
        values = [x[attr_name] for x in self.log_data]
        current_type = self.TrivialDomain.NULLABLE
        logger.info(f'deducing trivial type for \"{attr_name}\"...')
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

    def infer_common_statements(self, values, type_assignment):
        null_found = False
        deferred_init_detected = values[0] is None
        report_unique_entries = True
        unique_entries = set()
        statements = []

        for value in values:

            if value is None:
                null_found = True
            else:
                unique_entries.add(value)

            if type_assignment == self.TrivialDomain.INTEGER:
                if len(unique_entries) > self.INTEGER_CARDINALITY_LIMIT:
                    report_unique_entries = False
            elif type_assignment == self.TrivialDomain.STRING:
                if len(unique_entries) > self.STRING_CARDINALITY_LIMIT:
                    report_unique_entries = False

        ref_sequence = ReferencedSequence(values)
        ref_sequence.reduce_loops()
        if ref_sequence.is_pseudocyclic():
            if ref_sequence.is_cyclic():
                statements.append(Statement('CYCLED VALUES'))
            else:
                ratio = ref_sequence.get_stereotype_ratio()
                logger.info(f'detected stereotype ratio {ratio}')
                if ratio > self.STEREOTYPE_RATIO_THRESHOLD:
                    statements.append(Statement(
                        'PSEUDO CYCLIC WITH STEREOTYPE RATIO', ratio))

        if null_found:
            statements.append(Statement('CONTAINS NULLS'))

        if deferred_init_detected and unique_entries:
            statements.append(Statement('INITIALIZED AFTERWARDS'))

        # cardinal characteristics section
        if len(unique_entries) == len(values):
            statements.append(Statement('CARDINAL: CONTAINS UNIQUES'))

        if report_unique_entries and \
           (type_assignment == self.TrivialDomain.INTEGER or
            type_assignment == self.TrivialDomain.STRING):

            prepared = [str(x) for x in unique_entries]
            statements.append(Statement('CARDINAL: VALUES IN SET', *prepared))

        if len(unique_entries) == 1:
            statements.append(Statement('CARDINAL: CONTAINS STATIC', values[0]))

        return statements

    def dump_statements(self, attr_statements_list, output_file):
        if output_file:
            logger.info(f'dumping statements into {output_file}...')
            with open(output_file, mode='w', encoding='UTF-8') as output_stream:
                for pair in zip(self.attr_names, attr_statements_list):
                    prepared_statements = \
                        ';\n'.join(stmt.rjust(len(stmt)+2) for stmt in 
                                   [x.to_string() for x in pair[1]])
                    output_stream.write(f'{pair[0]}:\n'
                                        + prepared_statements + '\n')

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

        statements = [Statement('OF BASE TYPE', type_assignment)]
        if type_assignment != self.TrivialDomain.NULLABLE:
            statements += self.infer_common_statements(refined_values, 
                                                       type_assignment)

        if type_assignment == self.TrivialDomain.INTEGER:
            deduced = self.infer_statement_for_integer(refined_values)
        elif type_assignment == self.TrivialDomain.REAL:
            deduced = self.infer_statement_for_float(refined_values)
        elif type_assignment == self.TrivialDomain.BOOLEAN:
            deduced = self.infer_statement_for_boolean(refined_values)
        elif type_assignment == self.TrivialDomain.STRING:
            deduced = self.infer_statement_for_string(refined_values)
        else:
            deduced = Statement('NO ASSESSMENT FOR TYPE-INCONSISTENT DATA')

        return statements + (deduced if deduced 
                             else [Statement('NO SPECIFIC STATEMENTS')])

    def process_messages(self, dump_file=''):
        '''
        Generate statements for log attributes.

        The most general method for a heuristic. Dumps inferred statements to
        the console via logger and to the dump file if its name is specified.
        Appears as an entry point for further analysis. Meant to be a caller
        for the rest of methods.
        '''
        labeled_attributes = [self.get_global_attribute_statement(attr)
                              for attr in self.attr_names]
        logger.info('retrieved the following statements:')
        logger.info(pformat([(pair[0], [x.to_string() for x in pair[1]]) for pair
                             in zip(self.attr_names, labeled_attributes)], 
                             indent=2))
        if dump_file:
            self.dump_statements(labeled_attributes, dump_file)


if __name__ == '__main__':
    logger.info('running test method...')
    HeuristicBase.test_networkx()
