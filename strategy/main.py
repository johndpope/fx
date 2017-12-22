from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
from test_data_source import TestDataSource

from strategy import TestStrategy

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy)

    data = TestDataSource('2017-01-01T10:38:00Z', "2017-10-10T10:38:00Z")
    cerebro.adddata(data)
    cerebro.broker.setcash(2000)
    from matplotlib.dates import *

    cerebro.run()


    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
