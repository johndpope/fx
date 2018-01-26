from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

import backtrader as bt
import pycommon

from live_data_source import LiveDataSource
from test_data_source import TestDataSource

from strategy import TestStrategy



def init_log():
    logger = pycommon.LogBuilder()
    logger.init_rotating_file_handler("/var/log/fxservice")
    logger.init_stream_handler()
    logger.build()

init_log()

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy)

    data = TestDataSource('2017-01-01T10:38:00Z', "2017-01-30T10:38:00Z")
    # data = LiveDataSource()
    cerebro.adddata(data)
    cerebro.broker.setcash(2000)
    from matplotlib.dates import *

    cerebro.run()


    logging.debug('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
