from pprint import pformat

import logger as lg
from datastructures.statement import Statement
from procedures.heuristic_base import HeuristicBase

DEFAULT_STATEMENTS_DUMP_FILE = 'output/statements_dump/sequence_oriented.txt'
logger = lg.get_logger('HEL')


class SequenceOriented(HeuristicBase):

    STABILIZATION_RATE_THRESHOLD = 2

    def _infer_numeric_statements(self, values):
        '''
        Generate statements common for both INTEGER and REAL types.
        '''
        is_alternating = True
        monotonic_info = {
            'flag': True,
            'inc_dec': None,
        }
        bounds = {
            'from': None,
            'to': None,
        }
        previous = None

        def sign(value):
            return value > 0

        for item in values:
            if previous is not None:
                if is_alternating and (sign(item) == sign(previous)):
                    is_alternating = False
                if monotonic_info['flag']:
                    direction = monotonic_info['inc_dec']
                    if direction:
                        if (direction == 'INC' and not item > previous) or \
                           (direction == 'DEC' and not item < previous):

                            monotonic_info['flag'] = False
                    else:
                        monotonic_info['inc_dec'] = 'INC' if item > previous \
                                                    else 'DEC'
                if item < bounds['from']:
                    bounds['from'] = item
                if item > bounds['to']:
                    bounds['to'] = item
            else:
                bounds['from'] = item
                bounds['to'] = item

            previous = item

        statements = [Statement('VALUES IN RANGE', bounds['from'], bounds['to'])]
        if is_alternating:
            statements.append(Statement('ALTERNATING'))
        if monotonic_info['flag']:
            statements.append(Statement('MONOTONIC', monotonic_info['inc_dec']))
        return statements

    def infer_statement_for_integer(self, values):
        # Stabilization detection.
        # Statement is produced when the stabilization rate exceeds the 
        # `STABILIZATION_RATE_THRESHOLD`. The rate represents an extent of
        # delta shrinking and is calculated as an absolute delta between adjacent
        # elements at the beginning of a sequence divided by an adjacent elements
        # delta int the end of the collection. Sequence must be convergent in
        # order to produce such statement.
        logger.info('getting specific statements for INTEGER type attribute')
        is_stabilized = True
        is_constant_delta = True
        delta_at_beginning = None
        previous, previous_delta = None, None
        for item in values:
            print(item)
            if previous is not None:
                delta = abs(item-previous)
                if previous_delta is not None:
                    if delta != previous_delta:
                        is_constant_delta = False
                        if delta > previous_delta:
                            is_stabilized = False
                            break
                else:
                    delta_at_beginning = delta
                previous_delta = delta
            previous = item

        statements = self._infer_numeric_statements(values)
        if not delta or is_stabilized and delta and \
            delta_at_beginning/delta > self.STABILIZATION_RATE_THRESHOLD:

            statements.append(Statement('STABILIZES', delta_at_beginning, delta))

        # Id candidate detection
        explanatories = [x.explanatory for x in statements]
        if 'MONOTONIC' in explanatories and is_constant_delta:
            statements.append(Statement('ID CANDIDATE'))
        return statements

    def infer_statement_for_float(self, values):
        logger.info('getting specific statements for REAL type attribute')
        return self._infer_numeric_statements(values)

    def infer_statement_for_boolean(self, values):
        return None

    def infer_statement_for_string(self, values):
        return None

    def process_messages(self):
        labeled_attributes = [self.get_global_attribute_statement(attr)
                              for attr in self.attr_names]
        logger.info('retrieved the following statements:')
        logger.info(pformat([(pair[0], [x.to_string() for x in pair[1]]) for pair
                             in zip(self.attr_names, labeled_attributes)], 
                             indent=2))
        self.dump_statements(labeled_attributes, DEFAULT_STATEMENTS_DUMP_FILE)


# argv[1] is the file location for the JSON event data
if __name__ == '__main__':
    import json
    import sys

    if len(sys.argv) < 2:
        logger.error('JSON file should be passed as an argument '
                     + 'for the script. Aborting...')
        sys.exit(1)

    logger.info('directly running heuristic...')
    with open(sys.argv[1]) as json_data_stream:
        events = json.loads(json_data_stream.readline())
        if not events:
            logger.error('an empty event list has been passed. Aborting...')
            sys.exit(2)

        heuristic = SequenceOriented(events)
        heuristic.process_messages()
