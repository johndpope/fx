#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime as dt
import logging

import backtrader.feed as feed
from backtrader import date2num
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
            logging.debug(bar['time'])
        except StopIteration:
            return False

        self.l.datetime[0] = date2num(dt.datetime.strptime(bar['time'], '%Y-%m-%dT%H:%M:%SZ'))

        self.l.open[0] = (float(bar['bid_o']))
        self.l.high[0] = float(bar['bid_h'])
        self.l.low[0] = float(bar['bid_l'])
        self.l.close[0] = float(bar['bid_c'])
        self.l.volume[0] = float(bar['volume'])

        return True


class TestDataSource(feed.DataBase):

    def __init__(self, start, end):
        self.temp_arr = iter([])
        self.client = FxAPI('http://172.104.110.189:9000')
        self.generator = self.client.request(GetCandlesRequest(start, end, chunk=1000))

    def start(self):
        super(TestDataSource, self).start()

    def get_next(self):
        self.temp_arr = iter(next(self.generator))

    def _load(self):

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

        self.l.open[0] = (float(bar['bid_o']))
        self.l.high[0] = float(bar['bid_h'])
        self.l.low[0] = float(bar['bid_l'])
        self.l.close[0] = float(bar['bid_c'])
        self.l.volume[0] = float(bar['volume'])

        return True
