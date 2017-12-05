import logging

from influxdb import InfluxDBClient

from tick_data_service import TickDataService

from data_service_config import DataServiceConfig


class InfluxTickDataService(TickDataService):
    @classmethod
    def from_config(cls):
        cfg = DataServiceConfig()
        return InfluxTickDataService(cfg.DbHost, cfg.DbPort, cfg.DbUser, cfg.DbPass, 'ticks')

    def __init__(self, host, port, user, password, db_name):
        self.db_name = db_name
        self.password = password
        self.user = user
        self.host = host
        self.port = port

    def get_count(self):
        client = InfluxDBClient(self.host, self.port, self.user, self.password)
        client.create_database(self.db_name)
        client.switch_database(self.db_name)

        rs = client.query('SELECT COUNT(closeBid) FROM ticks')

        return list(rs)[0][0]['count']

    def get_lasted_bar(self, default_value=None):
        logging.debug("Get lasted time from host")
        client = InfluxDBClient(self.host, self.port, self.user, self.password)
        client.create_database(self.db_name)
        client.switch_database(self.db_name)

        rs = client.query('SELECT * FROM ticks ORDER BY DESC LIMIT 1')
        ls = list(rs)
        result = default_value
        if len(ls) > 0:
            result = ls[0][0]
        logging.debug(result)
        return result

    def get_bars(self, start, end):
        logging.debug("Get time from host")
        client = InfluxDBClient(self.host, self.port, self.user, self.password, self.db_name)
        rs = client.query("select * from ticks where time>'{}' and time < '{}'".format(start, end))
        ls = list(rs)
        return ls[0]

    def push_data(self, candles):
        logging.debug("push data to host")
        client = InfluxDBClient(self.host, self.port, self.user, self.password)
        client.create_database(self.db_name)
        client.switch_database(self.db_name)
        assert client.write_points(candles) == True

# fx_service = FxDataService(pycommon.get_env_or_config('host'), 8086)
# print(len(fx_service.get_bars('2017-08-01T10:38:00Z','2017-11-02T10:38:00Z')))
# print(fx_service.get_lasted_bar(None))
# print(len(fx_service.get_bars('2000-01-01T10:38:00Z','2017-11-02T10:38:00Z')))
