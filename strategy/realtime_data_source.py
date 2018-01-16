#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime as dt
import logging

import backtrader.feed as feed
from backtrader import date2num

import backtrader.feed as feed
from backtrader import date2num
from fxclient.fxapi import FxAPI
from fxclient.endpoints.stream_candle_request import StreamCandleRequest


class TestDataSource(feed.DataBase):


    def haslivedata(self):
        return True

    def islive(self):
        return True

    def __init__(self, start, end):
        self.temp_arr = iter([])
        self.client = FxAPI('http://172.104.110.189:9000')
        self.generator = self.client.request(StreamCandleRequest(start, end, chunk=1000))

    def start(self):
        super(TestDataSource, self).start()

    def get_next(self):
        self.temp_arr = iter(next(self.generator))

    def _load(self):

        while True:
            try:
                bar = next(self.temp_arr)
                logging.debug(bar['time'])
            except StopIteration:
                try:
                    logging.debug('fetch from service')
                    self.temp_arr = iter(next(self.generator))
                    bar = next(self.temp_arr)
                except StopIteration:
                    return False

            self.l.datetime[0] = date2num(dt.datetime.strptime(bar['time'], '%Y-%m-%dT%H:%M:%SZ'))

            self.l.open[0] = (float(bar['openBid']))
            self.l.high[0] = float(bar['highBid'])
            self.l.low[0] = float(bar['lowBid'])
            self.l.close[0] = float(bar['closeBid'])
            self.l.volume[0] = float(bar['volume'])

            self.put_notification(self.LIVE)
            return True
