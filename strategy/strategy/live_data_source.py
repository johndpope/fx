#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime as dt
import logging

import backtrader.feed as feed
from backtrader import date2num
from fxclient.fxapi import FxAPI
from fxclient.endpoints.stream_candle_request import StreamCandleRequest


class LiveDataSource(feed.DataBase):
    def haslivedata(self):
        return True

    def islive(self):
        return True

    def __init__(self):
        self.temp_arr = iter([])
        self.client = FxAPI('http://172.104.110.189:9000')
        self.generator = self.client.request(StreamCandleRequest())

    def start(self):
        super(LiveDataSource, self).start()

    def get_next(self):
        self.temp_arr = iter(next(self.generator))

    def _load(self):
        bar = next(self.generator)['candles'][0]

        logging.debug(bar)
        if bar:
            bar['time'] = bar['time'].replace('.000000000', '')
            self.l.datetime[0] = date2num(dt.datetime.strptime(bar['time'], '%Y-%m-%dT%H:%M:%SZ'))

            self.l.open[0] = (float(bar['bid']['o']))
            self.l.high[0] = float(bar['bid']['h'])
            self.l.low[0] = float(bar['bid']['l'])
            self.l.close[0] = float(bar['bid']['c'])
            self.l.volume[0] = float(bar['volume'])

            self.put_notification(self.LIVE)
            return True
