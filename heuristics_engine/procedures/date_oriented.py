from datetime import datetime as dt
import dateutil.parser as dateparser

import logger as lg
from datastructures.statement import Statement
from procedures.heuristic_base import HeuristicBase

DEFAULT_STATEMENTS_DUMP_FILE = 'output/statements_dump/date_oriented.txt'
logger = lg.get_logger('HEL')


class DateOriented(HeuristicBase):

    FAILED_PARSINGS_LIMIT = 5
    PATTERNS = [
        '%Y %b %d',
        '%Y %b %d %H:%M:%S',
        '%Y %B %d',
        '%Y %B %d %H:%M:%S',
        '%Y/%m/%d',
        '%Y/%m/%d %H:%M:%S',
        '%x',
    ]

    @staticmethod
    def _try_retrieve_timestamp(value: int):
        try:
            return dt.fromtimestamp(value)
        except OSError:
            logger.error(f'given value ({value}) is too large for timestamp')
            return

    @staticmethod
    def _try_datetime_parsing(raw: str):
        try:
            return dateparser.isoparse(raw)
        except ValueError:
            parsed = None

        for pattern in DateOriented.PATTERNS:
            try:
                parsed = dt.strptime(raw, pattern)
                break
            except ValueError:
                continue

        logger.error(f'unable to process string "{raw}" as a date[time]')
        return parsed 

    @staticmethod
    def _get_temporal_sequence(values):
        '''
        Convert given sequence into the list of `datetime` objects.
        '''
        result = []
        if not values:
            logger.error('cannot process empty sequence')
            return result
        else:
            underlying_type = type(values[0])

        logger.info(f'converting sequence of "{underlying_type.__name__}" '
                    + 'items into temporal sequence')
        failed_parsings = 0
        for item in values:
            if failed_parsings > DateOriented.FAILED_PARSINGS_LIMIT:
                log.error('too much elements have failed to be converted into'
                          + 'datetime objects, aborting...')
                break

            if underlying_type is int:
                temporal = DateOriented._try_retrieve_timestamp(item)
                if temporal:
                    result.append(temporal)
                else:
                    failed_parsings += 1
            elif underlying_type is str:
                try:
                    temporal = DateOriented._try_retrieve_timestamp(float(item))
                    if temporal:
                        result.append(temporal)
                    else:
                        failed_parsings += 1
                except ValueError:
                    parsed = DateOriented._try_datetime_parsing(item)
                    if parsed:
                        result.append(parsed)
                    else:
                        failed_parsings += 1
            else:
                logger.error(f'provided type ({underlying_type.__name__}) cannot'
                             'be transformed into temporal-like, aborting...')
                break

        if failed_parsings:
            logger.warn(f'{failed_parsings} out of {len(values)} elements have '
                        + 'been ignored and not added to the temporal sequence')
        return result

    def infer_statement_for_integer(self, values):
        logger.info('getting specific statements for INTEGER type attribute')
        datetimes = self._get_temporal_sequence(values)
        print(datetimes)
        return None

    def infer_statement_for_float(self, values):
        return None

    def infer_statement_for_boolean(self, values):
        return None

    def infer_statement_for_string(self, values):
        logger.info('getting specific statements for STRING type attribute')
        datetimes = self._get_temporal_sequence(values)
        print(datetimes)
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
