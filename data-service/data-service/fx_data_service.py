import logging

import pycommon
from influxdb import InfluxDBClient


class FxDataService:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get_lasted_bar(self, default_value):
        logging.debug("Get lasted time from host")
        client = InfluxDBClient(self.host, self.port, 'root', 'root', None)
        client.create_database('ticks')
        client.switch_database('ticks')

        rs = client.query('SELECT * FROM ticks ORDER BY DESC LIMIT 1')
        ls = list(rs)
        if len(ls) == 0:
            return default_value
        return ls[0][0]

    def get_bars(self, start, end):
        logging.debug("Get time from host")
        client = InfluxDBClient(self.host, self.port, 'root', 'root', 'ticks')
        rs = client.query("select * from ticks where time>'{}' and time < '{}'".format(start, end))
        ls = list(rs)
        return ls[0]

    def push_data(self, candles):
        logging.debug("push data to host")
        client = InfluxDBClient(self.host, self.port, 'root', 'root', None)
        client.create_database('ticks')
        client.switch_database('ticks')
        client.write_points(candles)

# fx_service = FxDataService(pycommon.get_env_or_config('host'), 8086)
# print(len(fx_service.get_bars('2017-08-01T10:38:00Z','2017-11-02T10:38:00Z')))
# print(fx_service.get_lasted_bar())
