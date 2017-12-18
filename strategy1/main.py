from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

import backtrader as bt
from fxclient.fxclient.api import API
from fxclient.fxclient.get_data_request import GetDataRequest

from strategy1.datasource import DataSource
from strategy1.strategy import TestStrategy

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '../../datas/orcl-1995-2014.txt')

    # Create a Data Feed
    client = API('http://172.104.110.189:9000')
    x = client.request(GetDataRequest('2017-08-01T10:38:00Z', "2017-08-02T10:38:00Z"))
    data = DataSource(x)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()
    cerebro.plot()
    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
