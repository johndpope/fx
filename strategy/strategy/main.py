from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

import backtrader as bt
import pycommon

from fxclient.data.live_data_source import LiveDataSource
from fxclient.data.test_data_source import TestDataSource
from fxclient.data.test_data_source_list import TestDataSourceList

from strategies.strategy import Strategy


def init_log():
    logging.getLogger("root").setLevel(logging.ERROR)

    logger = pycommon.LogBuilder()
    logger.init_rotating_file_handler("/var/log/strategy")
    logger.init_stream_handler()
    logger.build()


init_log()

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # cerebro.addstrategy(Strategy)
    cerebro.optstrategy(
        Strategy,
        trade_volume=[100],
        close_bar=[150,200,250,500]

    )

    data = TestDataSourceList('2017-01-01T10:38:00Z', "2017-01-05T10:38:00Z")
    # data = LiveDataSource()
    cerebro.adddata(data)
    cerebro.broker.setcash(10000)
    from matplotlib.dates import *

    # Run over everything
    stratruns = cerebro.run()

    print('==================================================')
    for stratrun in stratruns:
        print('**************************************************')
        for strat in stratrun:
            print('--------------------------------------------------')
            print(str(strat.p._getkwargs())  )

    print('==================================================')

    # logging.debug('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # cerebro.plot()
