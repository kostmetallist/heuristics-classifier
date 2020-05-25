import logger as lg
from procedures.heuristic_base import HeuristicBase

logger = lg.get_logger('HEL')


class Heuristic1(HeuristicBase):

    def get_global_attribute_statement(self, attr_name):
        return self.deduce_attribute_type(attr_name)[0]

    def process_messages(self):
        labeled_attributes = [self.get_global_attribute_statement(attr)
                              for attr in self.attr_names]
        logger.info('retrieved the following statements: '
                    + f'{[x for x in zip(self.attr_names, labeled_attributes)]}')
        return labeled_attributes


if __name__ == '__main__':
    import json
    import sys
    logger.info('directly running heuristic...')
    with open(sys.argv[1]) as json_data_stream:
        events = json.loads(json_data_stream.readline())
        if not events:
            logger.error('an empty event list has been passed. Aborting...')
            sys.exit(1)

        h = Heuristic1(events)
        h.process_messages()

