from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt

from strategy import TestStrategy
from realtime_data_source import TestDataSource

from live_data_source import LiveDataSource

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy)

    # data = TestDataSource('2017-01-01T10:38:00Z', "2017-01-05T10:38:00Z")
    data = LiveDataSource('2017-01-01T10:38:00Z', "2017-01-05T10:38:00Z")
    cerebro.adddata(data)
    cerebro.broker.setcash(2000)
    from matplotlib.dates import *

    cerebro.run()


    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # cerebro.plot()
