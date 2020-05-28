from pprint import pformat

import logger as lg
from procedures.heuristic_base import HeuristicBase

DEFAULT_STATEMENTS_DUMP_FILE = 'output/statements_dump/sequence_oriented.txt'
logger = lg.get_logger('HEL')


class SequenceOriented(HeuristicBase):

    def _dump_statements(self, 
                         statements_list, 
                         output_file=DEFAULT_STATEMENTS_DUMP_FILE):
        if output_file:
            logger.info(f'dumping statements into {output_file}...')
            with open(output_file, mode='w', encoding='UTF-8') as output_stream:
                for pair in zip(self.attr_names, statements_list):
                    output_stream.write(f'{pair[0]}:\n'
                                        + "\n".join([stripped.rjust(len(stripped)+2)
                                                     for stripped in [x.strip()
                                                                      for x in pair[1].split(";")]])
                                        + '\n')

    def infer_statement_for_integer(self, values):
        return ''

    def infer_statement_for_float(self, values):
        return ''

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
