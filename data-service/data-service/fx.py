import traceback

import oandapy

token = '5155f61a12f50401aed005d121b524f3-b9a736e4104e81e450556ad1345520c1'

oanda = oandapy.API(environment="practice", access_token=token)
from influxdb import InfluxDBClient

client = InfluxDBClient('172.104.110.189', 8086, 'root', 'root', 'ticks')
client.create_database('ticks')

rs = client.query("select count(*) from ticks where time>'2017-08-04' and time < '2017-09-04' ")
ls = list(rs.get_points())
print(ls)

# time = '2000-01-01'
#
# while True:
#     try:
#         data = oanda.get_history(instrument='EUR_USD',  # our instrument
#                                  start=time,  # start data
#                                  count=5000,
#                                  granularity='M1')  # minute bars  # 7
#         candles = data['candles']
#         time = candles[-1]['time']
#         converted = []
#         for v in candles:
#             converted.append({
#                 "measurement": "ticks",
#                 "time": v['time'],
#                 "fields": {
#                     'closeAsk': v['closeAsk'],
#                     'closeBid': v['closeBid'],
#                     'highAsk': v['highAsk'],
#                     'highBid': v['highBid'],
#                     'lowAsk': v['lowAsk'],
#                     'lowBid': v['lowBid'],
#                     'openAsk': v['openAsk'],
#                     'openBid': v['openBid'],
#                     'volume': v['volume'],
#                     'time': v['time']
#                 }
#             }
#             )
#         client.write_points(converted)
#         print(time + " " + str(len(candles)))
#     except:
#         print(traceback.format_exc())
