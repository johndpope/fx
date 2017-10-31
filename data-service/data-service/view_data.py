import logging

import oandapy

token = '5155f61a12f50401aed005d121b524f3-b9a736e4104e81e450556ad1345520c1'

oanda = oandapy.API(environment="practice", access_token=token)
from influxdb import InfluxDBClient

logging.debug("helo")

client = InfluxDBClient('172.104.110.189', 8086, 'root', 'root', 'ticks')

rs = client.query("select count(*) from ticks where time>'2009-01-01' and time < '2009-03-02' ")
# rs = client.query("SELECT * FROM ticks where time >= '2016-01-01 00:00:00' and time < '2016-02-01 00:00:00'")
ls = list(rs.get_points())
print(ls)
exit()
