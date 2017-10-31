import logging
import traceback

import oandapy
import pycommon
from influxdb import InfluxDBClient

pycommon.init_rotating_file("/fx/logs/")


def get_lasted_time():
    logging.debug("Get lasted time from host")
    client = InfluxDBClient(pycommon.get_env_or_config('host'), 8086, 'root', 'root', 'ticks')
    client.create_database('ticks')
    rs = client.query('SELECT * FROM ticks ORDER BY DESC LIMIT 1')
    ls = list(rs)
    if len(ls) == 0:
        return '2000-01-01'
    return ls[0][0]['time']


def push_data(candles):
    logging.debug("push data to host")
    client = InfluxDBClient(pycommon.get_env_or_config('host'), 8086, 'root', 'root', 'ticks')
    client.create_database('ticks')
    client.write_points(candles)


def get_from_odana(lasted_time):
    logging.debug("get data from odana")
    oanda = oandapy.API(environment="practice", access_token=pycommon.get_env_or_config('odanakey'))
    data = oanda.get_history(instrument='EUR_USD',  # our instrument
                             start=lasted_time,  # start data
                             count=5000,
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


while True:
    try:
        time = get_lasted_time()
        data = get_from_odana(time)
        push_data(data)

        logging.info("Success:" + time + " " + str(len(data)))
    except:
        logging.error(traceback.format_exc())
