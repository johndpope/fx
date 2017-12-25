import json
import logging

import backtrader as bt
from oandapyV20 import API, V20Error
from oandapyV20.endpoints import orders, positions

accountID, access_token = '101-011-6388580-003', 'c59ac783885ec75d0b147e730f820997-17fc99e689f2edb65ecb07060a914e71'
lasted_trade = None
logger = logging.getLogger(__name__)


def close():
    logger.info("Close existing positions ...")
    r = positions.PositionDetails(accountID=accountID,
                                  instrument='EUR_USD')
    api = API(access_token=access_token)

    try:
        openPos = api.request(r)

    except V20Error as e:
        logger.error("V20Error: %s", e)

    else:
        toClose = {}
        for P in ["long", "short"]:
            if openPos["position"][P]["units"] != "0":
                toClose.update({"{}Units".format(P): "ALL"})

        logger.info("prepare to close: {}".format(json.dumps(toClose)))
        r = positions.PositionClose(accountID=accountID,
                                    instrument="EUR_USD",
                                    data=toClose)
        rv = None
        try:
            if toClose:
                rv = api.request(r)
                logger.info("close: response: %s",
                            json.dumps(rv, indent=2))

        except V20Error as e:
            logger.error("V20Error: %s", e)


def by_test():
    api = API(access_token=access_token)
    r = orders.OrderCreate(accountID=accountID, data={
        "order": {
            "units": "100",
            "instrument": "EUR_USD",
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT"
        }
    })
    response = api.request(r)
    logging.debug(response)


# by_test()
# import time
# time.sleep(10)
# close()


class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        logging.debug('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = 5000
        self.c = True

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                # self.by_test()

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):

        # if self.c:
        #     by_test()
        # else:
        #     close()
        # self.c=not self.c
        # return

        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] < self.dataclose[-1]:
                # current close less than previous close

                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than the previous close

                    # BUY, BUY, BUY!!! (with default parameters)
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])

                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.buy(size=500)

        else:

            # Already in the market ... we might sell
            if len(self) >= (self.bar_executed + 500):
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell(size=500)
