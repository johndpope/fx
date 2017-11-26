import datetime
import logging

import dateutil
import oandapy

from crawl_service.crawl_service import CrawlService
from data_service_config import DataServiceConfig


class OandaCrawl(CrawlService):
    @classmethod
    def from_config(cls):
        cfg = DataServiceConfig()
        return OandaCrawl(cfg.OandaKey)

    def __init__(self, api_key):
        self.api_key = api_key

    def get(self, time, num_bars=5000, time_delta=60):
        dt = dateutil.parser.parse(time)
        dt = dt + datetime.timedelta(seconds=time_delta)
        dt = str(dt.isoformat())
        dt = dt.replace('+00:00', 'Z')
        logging.debug("get data from odana")

        oanda = oandapy.API(environment="practice", access_token=self.api_key)
        data = oanda.get_history(instrument='EUR_USD',  # our instrument
                                 start=dt,  # start data
                                 count=num_bars,
                                 granularity='M1')  # minute bars  # 7
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
