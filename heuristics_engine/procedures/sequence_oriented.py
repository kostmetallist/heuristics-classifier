import logger as lg
from procedures.heuristic_base import HeuristicBase

logger = lg.get_logger('HEL')


class SequenceOriented(HeuristicBase):

    def get_global_attribute_statement(self, attr_name):
        return self.deduce_attribute_type(attr_name)['type_assignment']

    def process_messages(self):
        labeled_attributes = [self.get_global_attribute_statement(attr)
                              for attr in self.attr_names]
        logger.info('retrieved the following statements: '
                    + f'{[x for x in zip(self.attr_names, labeled_attributes)]}')
        return labeled_attributes


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
