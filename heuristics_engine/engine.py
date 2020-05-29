#!/usr/bin/python3
import logger as lg
from procedures.heuristic_base import HeuristicBase
from procedures import sequence_oriented

HEURISTIC_MAPPINGS = {
    'sequence-oriented': sequence_oriented.SequenceOriented,
}
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

            default_heuristic_name = 'sequence-oriented'
            try:
                heuristic_class = HEURISTIC_MAPPINGS[sys.argv[2]]
                logger.info(f'calling {sys.argv[2]} heuristic...')
                heuristic = heuristic_class(events)

            except IndexError:
                logger.info('no heuristic name has been specified, '
                            + f'running {default_heuristic_name} heuristic...')
                heuristic = HEURISTIC_MAPPINGS[default_heuristic_name](events)
            except KeyError:
                logger.info('no matching heuristic has been found for the '
                            + f'passed name, running {default_heuristic_name} '
                            + 'heuristic...')
                heuristic = HEURISTIC_MAPPINGS[default_heuristic_name](events)
            finally:
                heuristic.process_messages()

    logger.info('shutting down heuristics engine...')
