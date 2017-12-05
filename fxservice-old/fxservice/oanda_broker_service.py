import datetime
import logging

import dateutil
import oandapy
from broker_service import BrokerService
from data_service_config import DataServiceConfig
from oandapyV20 import API
from oandapyV20.endpoints.accounts import AccountSummary


class OandaBrokerService(BrokerService):
    @classmethod
    def from_config(cls):
        cfg = DataServiceConfig()
        return OandaBrokerService(cfg.OandaKey)

    def __init__(self, api_key):
        self.api_key = api_key

    def get_profit_loss(self, account_id):
        access_token = "0cd4c62c9ea093e77c2086fcc61053ed-19807c1fb8c8e289298d7f9ae3351a72"
        r = AccountSummary(account_id)
        api = API(access_token=access_token, environment="practice")
        re = api.request(r)
        return re

    def get_bar(self, time, num_bars=5000, time_delta=60):
        dt = dateutil.parser.parse(time)
        dt = dt + datetime.timedelta(seconds=time_delta)
        dt = str(dt.isoformat())
        dt = dt.replace('+00:00', 'Z')
        logging.debug("get data from odana")

        oanda = oandapy.API(environment="practice", access_token=self.api_key)
        data = oanda.get_history(instrument='EUR_USD',  # our instrument
                                 start=dt,  # start data
                                 count=num_bars,
                                 granularity='S5')  # minute bars  # 7
        candles = data['candles']
        converted = []

        for v in candles:
            converted.append({
                "measurement": "ticks",
                "time": v['time'],
                "fields": {
                    'closeAsk': v['closeAsk'],
                    'closeBid': v['closeBid'],
                    'highAsk': v['highAsk'],
                    'highBid': v['highBid'],
                    'lowAsk': v['lowAsk'],
                    'lowBid': v['lowBid'],
                    'openAsk': v['openAsk'],
                    'openBid': v['openBid'],
                    'volume': v['volume'],
                    'time': v['time']
                }
            })
        return converted
