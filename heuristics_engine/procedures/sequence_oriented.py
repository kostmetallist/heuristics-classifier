from pprint import pformat

import logger as lg
from datastructures.statement import Statement
from procedures.heuristic_base import HeuristicBase

DEFAULT_STATEMENTS_DUMP_FILE = 'output/statements_dump/sequence_oriented.txt'
logger = lg.get_logger('HEL')


class SequenceOriented(HeuristicBase):

    # STATEMENTS = {
    #     'accumulative': 'ACCUMULATIVE',
    #     'alternating': 'ALTERNATING',
    #     'id_candidate': 'ID CANDIDATE',
    #     'in_range': 'VALUES IN RANGE',
    #     'monotonic': 'MONOTONIC',
    # }

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
        statements = self._infer_numeric_statements(values)
        return statements

    def infer_statement_for_float(self, values):
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
