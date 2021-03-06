import logging

import pycommon
from influxdb import InfluxDBClient

from .tick_data_service import TickDataService


class InfluxTickDataService(TickDataService, pycommon.patterns.Publisher):
    @classmethod
    def from_config(cls):
        from config import DataServiceConfig
        cfg = DataServiceConfig()
        return InfluxTickDataService(cfg.DbHost, cfg.DbPort, cfg.DbUser, cfg.DbPass, cfg.DbName)

    def __init__(self, host, port, user, password, db_name):
        pycommon.patterns.Publisher.__init__(self, ['added'])
        self.db_name = db_name
        self.password = password
        self.user = user
        self.host = host
        self.port = port

    def reset(self):
        client = InfluxDBClient(self.host, self.port, self.user, self.password)
        client.drop_database(self.db_name)

    def get_count(self):
        client = InfluxDBClient(self.host, self.port, self.user, self.password)
        client.create_database(self.db_name)
        client.switch_database(self.db_name)

        rs = client.query('SELECT COUNT(volume) FROM {}'.format(self.db_name))

        data = list(rs)

        if len(data) == 0 or len(data[0]) == 0 or 'count' not in data[0][0]:
            return 0

        return list(rs)[0][0]['count']

    def get_lasted_bar(self, default_value=None):
        logging.debug("Get lasted time from host")
        client = InfluxDBClient(self.host, self.port, self.user, self.password)
        client.create_database(self.db_name)
        client.switch_database(self.db_name)

        rs = client.query('SELECT * FROM {} ORDER BY DESC LIMIT 1'.format(self.db_name))
        ls = list(rs)
        result = default_value
        if len(ls) > 0:
            result = ls[0][0]
        logging.debug(result)
        return result

    def get_bars(self, start, end):
        logging.debug("Get time from host")
        client = InfluxDBClient(self.host, self.port, self.user, self.password, self.db_name)
        rs = client.query("select * from {} where time>'{}' and time < '{}'".format(self.db_name, start, end))
        ls = list(rs)
        return ls[0]

    def push_data(self, candles):
        logging.debug("push data to host")

        converted = []

        for v in candles['candles']:
            v.pop('complete')

            converted.append({
                "measurement": self.db_name,
                "time": v['time'],
                "fields": {
                    "volume": v['volume'],

                    "bid_o": v['bid']['o'],
                    "bid_c": v['bid']['c'],
                    "bid_h": v['bid']['h'],
                    "bid_l": v['bid']['l'],

                    "ask_o": v['ask']['o'],
                    "ask_c": v['ask']['c'],
                    "ask_h": v['ask']['h'],
                    "ask_l": v['ask']['l']
                }
            })
        logging.debug(converted[0]['time'])

        client = InfluxDBClient(self.host, self.port, self.user, self.password)
        client.create_database(self.db_name)
        client.switch_database(self.db_name)
        assert client.write_points(converted) is True
        super().dispatch('added', candles)

# fx_service = FxDataService(pycommon.get_env_or_config('host'), 8086)
# logging.debug(len(fx_service.get_bars('2017-08-01T10:38:00Z','2017-11-02T10:38:00Z')))
# logging.debug(fx_service.get_lasted_bar(None))
# logging.debug(len(fx_service.get_bars('2000-01-01T10:38:00Z','2017-11-02T10:38:00Z')))
