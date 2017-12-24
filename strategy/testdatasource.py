#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime as dt

import backtrader.feed as feed
from backtrader import date2num
from fxclient.fxclient.fxapi import API
from fxclient.fxclient.get_data_request import GetDataRequest


class TestDataSource(feed.DataBase):

    def __init__(self, data):
        self.data = iter(data)

    @classmethod
    def download_from_service(cls, service, start, end):
        client = API(service)
        data = client.request(GetDataRequest(start, end))
        return TestDataSource(data)

    def start(self):
        super(TestDataSource, self).start()

    def _load(self):
        try:
            bar = next(self.data)
        except StopIteration:
            return False

        self.l.datetime[0] = date2num(dt.datetime.strptime(bar['time'],
                                                           '%Y-%m-%dT%H:%M:%SZ'))

        self.l.open[0] = (float(bar['openBid']))
        self.l.high[0] = float(bar['highBid'])
        self.l.low[0] = float(bar['lowBid'])
        self.l.close[0] = float(bar['closeBid'])
        self.l.volume[0] = float(bar['volume'])
        return True
