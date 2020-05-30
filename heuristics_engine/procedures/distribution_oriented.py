import warnings

import numpy as np
import scipy.stats as st

import logger as lg
from datastructures.statement import Statement
from procedures.heuristic_base import HeuristicBase

DEFAULT_STATEMENTS_DUMP_FILE = 'output/statements_dump/distribution_oriented.txt'
logger = lg.get_logger('HEL')


class DistributionOriented(HeuristicBase):

    DISTRIBUTIONS = [
        st.dweibull,
        st.erlang,
        st.expon,
        st.gamma,
        st.invweibull,
        st.laplace,
        st.norm,
        st.pareto,
        st.uniform,
        st.weibull_max,
        st.weibull_min,
    ]

    @staticmethod
    def _is_normalized_sequence(values):
        total = 0
        for item in values:
            total += item
            if not 0 < item < 1:
                return False
        return np.isclose(total, 1.0)

    def _get_fitting_distribution(self, values, bins=1000):

        y, x = np.histogram(values, bins=bins, density=True)
        x = (x + np.roll(x, -1))[:-1] / 2.0
        best_distribution = st.norm
        best_params = (0.0, 1.0)
        minimal_sse = np.inf

        for distribution in self.DISTRIBUTIONS:
            try:
                with warnings.catch_warnings():
                    # Ignore warnings from data which cannot be procedured
                    warnings.filterwarnings('ignore')
                    params = distribution.fit(values)
                    args = params[:-2]
                    pdf = distribution.pdf(x, loc=params[-2], scale=params[-1],
                                           *args)
                    sse = np.sum(np.power(y - pdf, 2.0))

                    if sse > 0 and sse < minimal_sse:
                        best_distribution = distribution
                        best_params = params
                        minimal_sse = sse

            except Exception:
                logger.error('unknown exception during distribution fit for '
                             + f'{distribution.name}')

        logger.info(f'chosen {best_distribution.name} due to minimal SSE '
                    + f'value of {minimal_sse}')
        return (best_distribution.name, [float(param) for param in best_params])

    def infer_statement_for_integer(self, values):
        logger.info('getting specific statements for INTEGER type attribute')
        distribution, params = self._get_fitting_distribution(values)
        return [Statement('OF DISTRIBUTION', distribution, *params)]

    def infer_statement_for_float(self, values):
        logger.info('getting specific statements for REAL type attribute')
        distribution, params = self._get_fitting_distribution(values)
        statements = [Statement('OF DISTRIBUTION', distribution, *params)]
        if self._is_normalized_sequence(values):
            statements.append(Statement('NORMALIZED'))
        return statements

    def infer_statement_for_boolean(self, values):
        return None

    def infer_statement_for_string(self, values):
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

        heuristic = DistributionOriented(events)
        heuristic.process_messages()
