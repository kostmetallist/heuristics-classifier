#!/usr/bin/python3
import logger as lg
from procedures.heuristic_base import HeuristicBase
from procedures import DateOriented, DistributionOriented, SequenceOriented 

HEURISTIC_MAPPINGS = {
    'date-oriented': DateOriented,
    'distribution-oriented': DistributionOriented,
    'sequence-oriented': SequenceOriented,
}

DEFAULT_HEURISTIC_NAME = 'sequence-oriented'
# stands for Heuristics Engine Logger
logger = lg.get_logger('HEL')


# argv[1] is the file location for the JSON event data
# argv[2] (optional) is the name of heuristic procedure to use
if __name__ == '__main__':
    import json
    import sys
    from os import path

    if len(sys.argv) < 2:
        logger.error('JSON file should be passed as an argument '
                     + 'for the script. Aborting...')
    else:
        logger.info(f'using {path.abspath(sys.argv[1])} as an input...')
        with open(sys.argv[1]) as json_data_stream:
            events = json.loads(json_data_stream.readline())
            if not events:
                logger.error('an empty event list has been passed. Aborting...')
                sys.exit(1)

            try:
                heuristic_class = HEURISTIC_MAPPINGS[sys.argv[2]]
                logger.info(f'calling {sys.argv[2]} heuristic...')
                heuristic = heuristic_class(events)

            except IndexError:
                logger.info('no heuristic name has been specified, '
                            + f'running {DEFAULT_HEURISTIC_NAME} heuristic...')
                heuristic = HEURISTIC_MAPPINGS[DEFAULT_HEURISTIC_NAME](events)
            except KeyError:
                logger.info('no matching heuristic has been found for the '
                            + f'passed name, running {DEFAULT_HEURISTIC_NAME} '
                            + 'heuristic...')
                heuristic = HEURISTIC_MAPPINGS[DEFAULT_HEURISTIC_NAME](events)
            finally:
                heuristic.process_messages()

    logger.info('shutting down heuristics engine...')
