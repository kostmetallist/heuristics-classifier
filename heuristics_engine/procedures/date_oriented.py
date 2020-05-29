from pprint import pformat

import logger as lg
from datastructures.statement import Statement
from procedures.heuristic_base import HeuristicBase


DEFAULT_STATEMENTS_DUMP_FILE = 'output/statements_dump/date_oriented.txt'
logger = lg.get_logger('HEL')


class DateOriented(HeuristicBase):
    def infer_statement_for_integer(self, values):
        return None

    def infer_statement_for_float(self, values):
        return None

    def infer_statement_for_boolean(self, values):
        return None

    def infer_statement_for_string(self, values):
        logger.info('getting specific statements for STRING type attribute')
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

        heuristic = DateOriented(events)
        heuristic.process_messages()
