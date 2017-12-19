from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
from testdatasource import TestDataSource

from strategy import TestStrategy

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy)
    data = TestDataSource.download_from_service('http://172.104.110.189:9000', '2017-07-01T10:38:00Z',
                                                "2017-07-05T10:38:00Z")
    cerebro.adddata(data)
    cerebro.broker.setcash(2000)
    from matplotlib.dates import *

    # Run over everything
    cerebro.run()

    # Print out the
    # final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
