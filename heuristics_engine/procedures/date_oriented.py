from datetime import datetime as dt
import dateutil.parser as dateparser
from collections import defaultdict
from functools import reduce

import logger as lg
from datastructures.statement import Statement
from procedures.heuristic_base import HeuristicBase

DEFAULT_STATEMENTS_DUMP_FILE = 'output/statements_dump/date_oriented.txt'
logger = lg.get_logger('HEL')


class DateOriented(HeuristicBase):

    FAILED_PARSINGS_LIMIT = 5
    PATTERNS = [
        '%Y/%m/%d',
        '%Y/%m/%d %H:%M:%S',
        '%Y/%m/%d:%H:%M:%S',
        '%d/%b/%Y:%H:%M:%S',
        '%d/%m/%Y %H:%M:%S',
        '%d-%m-%Y %H:%M',
        '%d-%m-%Y %H:%M:%S',
        '%Y %b %d',
        '%Y %b %d %H:%M:%S',
        '%Y %b %d:%H:%M:%S',
        '%Y %B %d',
        '%Y %B %d %H:%M:%S',
        '%Y %B %d:%H:%M:%S',
        '%x',
    ]
    PRECISION_RATES = [
        'microsecond',
        'second',
        'minute',
        'day',
        'month',
        'year',
    ]
    WEEKDAY_MAPPINGS = {
        0: 'MON', 1: 'TUE', 2: 'WED', 3: 'THU', 4: 'FRI', 5: 'SAT', 6: 'SUN',
    }
    MONTH_MAPPINGS = {
        1: 'JAN',
        2: 'FEB',
        3: 'MAR',
        4: 'APR',
        5: 'MAY',
        6: 'JUN',
        7: 'JUL',
        8: 'AUG',
        9: 'SEP',
        10: 'OCT',
        11: 'NOV',
        12: 'DEC',
    }
    MODE_THRESHOLD = .75

    @staticmethod
    def _try_retrieve_timestamp(value: int):
        try:
            return dt.fromtimestamp(value)
        except OSError:
            logger.warning(f'given value ({value}) is too large for timestamp')
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
                return parsed
            except ValueError:
                continue

        logger.warning(f'unable to process string "{raw}" as a date[time]')
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
            if item is None:
                continue
                
            if failed_parsings > DateOriented.FAILED_PARSINGS_LIMIT:
                logger.info('too much elements have failed to be converted into'
                            + ' datetime objects, aborting...')
                return

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
                logger.info(f'provided type ({underlying_type.__name__}) cannot'
                             ' be transformed into temporal-like, aborting...')
                return

        if failed_parsings:
            logger.warn(f'{failed_parsings} out of {len(values)} elements have '
                        + 'been ignored and not added to the temporal sequence')
        return result

    @staticmethod
    def _infer_temporal_statements(values):
        statements = []
        datetimes = DateOriented._get_temporal_sequence(values)
        if not datetimes:
            return []

        is_ordered = True
        precision = DateOriented.PRECISION_RATES[0]
        previous = None

        def get_precision_index(precision):
            try:
                index = DateOriented.PRECISION_RATES.index(precision)
                return index
            except ValueError:
                logger.error(f'invalid precision expression ({precision})')
                return

        def downgrade_precision(precision):
            index = get_precision_index(precision)
            if index:
                if index == len(DateOriented.PRECISION_RATES)-1:
                    return
                else:
                    precision = DateOriented.PRECISION_RATES[index+1]
                    return precision

        def is_greater_than(first, second, precision):
            index = get_precision_index(precision)
            if index:
                ignored_fields = DateOriented.PRECISION_RATES[:index]
                kwargs = {x: (0 if x in ['microsecond', 'second', 'minute'] 
                              else 1) for x in ignored_fields}
                return first.replace(**kwargs) > second.replace(**kwargs)

        for item in datetimes:
            if previous:
                while precision:
                    if is_greater_than(previous, item, precision):
                        precision = downgrade_precision(precision)
                    else:
                        break
                if not precision:
                    print(item)
                    logger.info('dates in a given temporal sequence are '
                              + 'not ordered consequentially')
                    is_ordered = False
                    break
            else:
                for rate in DateOriented.PRECISION_RATES:
                    if getattr(item, rate):
                        precision = rate
                        break
            previous = item

        if is_ordered:
            statements.append(Statement('VALID TEMPORAL SEQUENCE', precision))
        else:
            return statements

        for rate in DateOriented.PRECISION_RATES[get_precision_index(precision):]:
            items_by_rate = defaultdict(int)
            if rate == 'day':
                for item in datetimes:
                    items_by_rate[item.weekday()] += 1
            else:
                for item in datetimes:
                    items_by_rate[getattr(item, rate)] += 1

            mode = reduce(lambda x, y: x if x[1] > y[1] else y, 
                          items_by_rate.items())
            if mode:
                mode_ratio = mode[1]/len(datetimes)
            else:
                continue

            logger.info(f'fixed mode ratio {mode_ratio} for "{rate}" frequency')
            if mode_ratio > DateOriented.MODE_THRESHOLD:
                statement_explanatory = 'WITH MODE'
                if rate == 'day':
                    statements.append(Statement(
                        statement_explanatory, rate,
                        DateOriented.WEEKDAY_MAPPINGS[mode[0]]))
                elif rate == 'month':
                    statements.append(Statement(
                        statement_explanatory, rate, 
                        DateOriented.MONTH_MAPPINGS[mode[0]]))
                else:
                    statements.append(Statement(statement_explanatory, rate, 
                                                mode[0]))
        return statements

    def infer_statement_for_integer(self, values):
        logger.info('getting specific statements for INTEGER type attribute')
        return self._infer_temporal_statements(values)

    def infer_statement_for_float(self, values):
        return None

    def infer_statement_for_boolean(self, values):
        return None

    def infer_statement_for_string(self, values):
        logger.info('getting specific statements for STRING type attribute')
        return self._infer_temporal_statements(values)

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
