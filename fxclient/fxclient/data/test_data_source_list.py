import datetime as dt

from backtrader import feed as feed, date2num
from fxclient.endpoints.get_candles import GetCandlesRequest
from fxclient.fxapi import FxAPI


class TestDataSourceList(feed.DataBase):

    def __init__(self, start, end):
        self.arr = []

        self.client = FxAPI('http://172.104.110.189:9000')
        for v in self.client.request(GetCandlesRequest(start, end, chunk=1000)):
            for vv in v:
                self.arr.append(vv)
        print(len(self.arr))
        self.temp_arr = iter(self.arr)

    def start(self):
        super(TestDataSourceList, self).start()

    def get_next(self):
        self.temp_arr = iter(next(self.arr))

    def _load(self):

        try:
            bar = next(self.temp_arr)
        except StopIteration:
            return False

        self.l.datetime[0] = date2num(dt.datetime.strptime(bar['time'], '%Y-%m-%dT%H:%M:%SZ'))

        self.l.open[0] = (float(bar['bid_o']))
        self.l.high[0] = float(bar['bid_h'])
        self.l.low[0] = float(bar['bid_l'])
        self.l.close[0] = float(bar['bid_c'])
        self.l.volume[0] = float(bar['volume'])

        return True