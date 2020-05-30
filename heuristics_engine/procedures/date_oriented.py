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

    def process_messages(self, dump_file=DEFAULT_STATEMENTS_DUMP_FILE):
        super().process_messages(dump_file)


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
