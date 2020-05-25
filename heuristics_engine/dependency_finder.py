#!/usr/bin/python3
import logger as lg
from procedures.heuristic_base import HeuristicBase

# stands for Heuristics Engine Logger
logger = lg.get_logger('HEL')


# argv[1] is the file location for the JSON event data
# argv[2] (optional) is the name of heuristic procedure to use
if __name__ == '__main__':
    import json
    import sys
    from pprint import pprint 
    with open(sys.argv[1]) as json_data_stream:
        events = json.loads(json_data_stream.readline())
        pprint(events, indent=2)
        logger.info('calling heuristic_base.py...')
        hb = HeuristicBase()
        hb.test_networkx()

    logger.info('shutting down heuristics engine...')
