from procedures.heuristic_base import HeuristicBase
import logger as lg

logger = lg.get_logger('HEL')


class Heuristic1(HeuristicBase):

    def get_global_attribute_statement(self, attr_name):
        return 'stub'

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
    with open(sys.argv[1]) as jsonDataStream:
        events = json.loads(jsonDataStream.readline())
        if not events:
            logger.error('an empty event list has been passed. Aborting...')
            sys.exit(1)

        h = Heuristic1(events)
        h.process_messages()

