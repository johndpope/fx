from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

import backtrader as bt
import pycommon
from test_data_source import TestDataSource

from strategy import TestStrategy

logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.ERROR)
logging.getLogger("oandapyV20.oandapyV20").setLevel(logging.ERROR)

logger = pycommon.LogBuilder()
logger.init_stream_handler()
logger.build()

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy)

    data = TestDataSource('2011-01-01T10:38:00Z', "2011-01-05T10:38:00Z")
    # data = LiveDataSource('2017-01-01T10:38:00Z', "2017-01-05T10:38:00Z")
    cerebro.adddata(data)
    cerebro.broker.setcash(2000)

    cerebro.run()

    logging.debug('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
