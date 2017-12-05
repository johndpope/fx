import logging
import traceback

from influx_tick_data_service import InfluxTickDataService

logging.getLogger().setLevel(logging.INFO)
delay_time = 0
dst_host = 'http://172.104.110.189:9000'
src_host = '172.104.110.189'
src_port = 8086

data_service = InfluxTickDataService(host=src_host,
                                     port=src_port,
                                     user='root',
                                     password='root',
                                     db_name='ticks')
data = data_service.get_bars('2017-01-01', '2017-01-09')
print(len(data))
for v in data:
    import requests

    try:

        url = dst_host + "/push_data"
        import json

        payload = json.dumps([v])
        headers = {'content-type': 'application/json'}

        response = requests.request("POST", url, data=payload, headers=headers)
        print(json.loads(response.content))

    except:
        print(traceback.format_exc())
        pass
    import time

    time.sleep(delay_time)
