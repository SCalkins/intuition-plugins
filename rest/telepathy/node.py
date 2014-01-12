# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Xavier Bruhiere


from intuition.core.engine import Simulation
from intuition.utils.logger import log, get_nestedlog
import intuition.data.utils as datautils
import intuition.core.configuration as setup


def test_queue(name, ctx):
    return {'name': name, 'context': ctx}


def trade(session, ctx):
    log_setup = get_nestedlog(level='info', show_log=False)
    with log_setup.applicationbound():

        configuration, strategy = setup.context(ctx)
        if not configuration:
            log.error('unable to build context, aborting...')
            return {'error': 'unable to build context, aborting'}

        engine = Simulation(configuration)
        engine.configure()

        data = {'universe': configuration['universe'],
                'index': configuration['index']}
        analyzes = engine.run(session, data, strategy)

        if analyzes is None:
            log.error('backtest failed.')
            return {'error': 'backtest failed'}

        bm_symbol = datautils.Exchanges[configuration['exchange']]['symbol']

        # Get daily, cumulative and not, returns of portfolio and benchmark
        returns_df = analyzes.get_returns(benchmark=bm_symbol)

        orders = 0
        for order in analyzes.results.orders:
            orders += len(order)

        final_value = analyzes.results.portfolio_value[-1]
        report = {
            'portfolio': final_value,
            'gain': final_value - strategy['manager']['cash'],
            'orders': orders,
            'portfolio_perfs': returns_df['algo_c_return'][-1] * 100.0,
            'benchmark_perfs': returns_df['benchmark_c_return'][-1] * 100.0,
            'pnl_mean': analyzes.results.pnl.mean(),
            'pnl_deviation': analyzes.results.pnl.std(),
        }

        perfs = analyzes.overall_metrics('one_month')
        for k, v in perfs.iteritems():
            report[k] = v

        return report
