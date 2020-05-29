from pprint import pformat

import logger as lg
from procedures.heuristic_base import HeuristicBase

DEFAULT_STATEMENTS_DUMP_FILE = 'output/statements_dump/sequence_oriented.txt'
logger = lg.get_logger('HEL')


class SequenceOriented(HeuristicBase):

    STATEMENTS = {
        **HeuristicBase.STATEMENTS,
        'accumulative': 'ACCUMULATIVE',
        'alternating': 'ALTERNATING',
        'id_candidate': 'ID CANDIDATE',
        'in_range': 'VALUES IN RANGE',
        'monotonic': 'MONOTONIC',
    }

    def _dump_statements(self, 
                         statements_list, 
                         output_file=DEFAULT_STATEMENTS_DUMP_FILE):
        if output_file:
            logger.info(f'dumping statements into {output_file}...')
            with open(output_file, mode='w', encoding='UTF-8') as output_stream:
                for pair in zip(self.attr_names, statements_list):
                    prepared_statements = \
                        [stripped.rjust(len(stripped)+2)
                         for stripped in [x.strip() for x in pair[1].split(";")]]
                    output_stream.write(f'{pair[0]}:\n'
                                        + '\n'.join(prepared_statements) + '\n')

    def _infer_numeric_statements(self, values):
        '''
        Generate statments common for both INTEGER and REAL types.
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

        statements = [f'{self.STATEMENTS["in_range"]} '
                      + f'({bounds["from"]}, {bounds["to"]})']
        if is_alternating:
            statements.append(self.STATEMENTS['alternating'])
        if monotonic_info['flag']:
            statements.append(f'{self.STATEMENTS["monotonic"]} '
                              + f'({monotonic_info["inc_dec"]})')
        return '; '.join(statements)

    def infer_statement_for_integer(self, values):
        statements = self._infer_numeric_statements(values)
        # TODO
        return statements

    def infer_statement_for_float(self, values):
        statements = self._infer_numeric_statements(values)
        # TODO
        return statements

    def infer_statement_for_boolean(self, values):
        return ''

    def infer_statement_for_string(self, values):
        return ''

    def process_messages(self):
        labeled_attributes = [self.get_global_attribute_statement(attr)
                              for attr in self.attr_names]
        logger.info('retrieved the following statements:')
        logger.info(pformat([x for x 
                             in zip(self.attr_names, labeled_attributes)], 
                            indent=2))
        self._dump_statements(labeled_attributes)


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
