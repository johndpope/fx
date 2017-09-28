from datetime import datetime, timedelta
import traceback
import oandapy
import cfg_reader

token = '5155f61a12f50401aed005d121b524f3-b9a736e4104e81e450556ad1345520c1'

oanda = oandapy.API(environment="practice", access_token=token)
from influxdb import InfluxDBClient

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'ticks')
client.create_database('ticks')

rs = client.query("select * from ticks where time>'2017-08-04' and time < '2017-09-04' ")
ls = list(rs.get_points())

# response = oanda.get_prices(instruments="EUR_USD")
# prices = response.get("prices")
# asking_price = prices[0].get("ask")
# print(asking_price)

# required datetime functions


# # sample account_id
# account_id = 1813880
#
# # set the trade to expire after one day
# trade_expire = datetime.utcnow() + timedelta(days=1)
# trade_expire = trade_expire.isoformat("T") + "Z"
#
# response = oanda.create_order(account_id,
#                               instrument="USD_CAD",
#                               units=1000,
#                               side='sell',
#                               type='limit',
#                               price=1.15,
#                               expiry=trade_expire
#                               )

time = '2016-12-08'

while True:
    try:
        data = oanda.get_history(instrument='EUR_USD',  # our instrument
                                 start=time,  # start data
                                 count=5000,
                                 granularity='M1')  # minute bars  # 7
        candles = data['candles']
        time = candles[-1]['time']
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
            }
            )
        client.write_points(converted)
        print(time + " " + str(len(candles)))
    except:
        print(traceback.format_exc())
