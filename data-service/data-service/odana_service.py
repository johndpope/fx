import datetime
import logging

import dateutil.parser
import oandapy
import pycommon


class OdanaClient:
    def __init__(self, token):
        self.token = token

    def get_from_odana(self, lasted_time, count=1, time_delta=60):
        dt = dateutil.parser.parse(lasted_time)
        dt = dt + datetime.timedelta(seconds=time_delta)
        dt = str(dt.isoformat())
        dt = dt.replace('+00:00', 'Z')
        logging.debug("get data from odana")

        oanda = oandapy.API(environment="practice", access_token=self.token)
        data = oanda.get_history(instrument='EUR_USD',  # our instrument
                                 start=dt,  # start data
                                 count=count,
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

#
# client=OdanaClient(pycommon.get_env_or_config('odanakey'))
# print(client.get_from_odana('2017-11-02T10:39:00Z'))
# print(client.get_from_odana(str(datetime.datetime.now().utcnow().isoformat())))
