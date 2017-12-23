import argparse
import logging
import re

import oandapyV20.endpoints.instruments as instruments


class Downloader:
    def __init__(self, api, accountID):
        self._accountID = accountID
        self.api = api
        self.clargs = argparse.Namespace()
        self.clargs.count = 10
        self.clargs.granularity = 'M1'
        self.clargs.price = 'B'
        self.clargs.instruments = 'EUR_USD'
        self.clargs.From = None
        self.clargs.to = None

    def get_by_start_and_count(self, time, num_bars=5000):
        logging.debug("get data from odana")
        self.clargs.count = num_bars
        self.clargs.granularity = 'M1'
        self.clargs.price = 'BA'
        self.clargs.instruments = 'EUR_USD'
        self.clargs.From = time
        self.clargs.to = None

    def get_data(self):
        def check_date(s):
            dateFmt = "[\d]{4}-[\d]{2}-[\d]{2}T[\d]{2}:[\d]{2}:[\d]{2}Z"
            if not re.match(dateFmt, s):
                raise ValueError("Incorrect date format: ", s)

            return True

        if self.clargs.instruments:
            params = {}
            if self.clargs.granularity:
                params.update({"granularity": self.clargs.granularity})
            if self.clargs.count:
                params.update({"count": self.clargs.count})
            if self.clargs.From and check_date(self.clargs.From):
                params.update({"from": self.clargs.From})
            if self.clargs.to and check_date(self.clargs.to):
                params.update({"to": self.clargs.to})
            if self.clargs.price:
                params.update({"price": self.clargs.price})
            r = instruments.InstrumentsCandles(instrument=self.clargs.instruments, params=params)
            rv = self.api.request(r)
            return rv

# cfg = Config()
#
# m = Main(api=API(access_token=cfg.OandaKey), accountID=cfg.AccountId)
# m.get_by_start_and_count('2005-02-01T00:00:00Z', 1)
# print(m.get_data())
