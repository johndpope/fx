import logging
import traceback

import pycommon

from broker_service.oanda_broker_service import OandaBrokerService
from tick_data_service.influx_tick_data_service import InfluxTickDataService

logging.getLogger().setLevel(logging.INFO)

data_service = InfluxTickDataService.from_config()
data=data_service.get_bars('2017-01-01', '2017-01-09')
print(len(data))
for v in data:
    import requests

    try:

        url = "http://localhost:5000/push_data"
        import json

        payload = json.dumps([v])
        headers = {'content-type': 'application/json'}

        response = requests.request("POST", url, data=payload, headers=headers)
        print(json.loads(response.content))
    except:
        pass
    import time

    time.sleep(0)

exit(0)


class Sync(pycommon.patterns.Publisher):
    @classmethod
    def default(cls):
        data_service = InfluxTickDataService.from_config()
        broker_service = OandaBrokerService.from_config()
        return Sync(data_service, broker_service)

    def __init__(self, data_service, broker_service):
        super(Sync, self).__init__(['tick', 'added'])
        self.data_service = data_service
        self.broker_service = broker_service

    def start(self):
        while True:
            logging.debug('Get data')
            try:
                time = self.data_service.get_lasted_bar({'time': '2000-01-01'})['time']
                try:
                    data = self.broker_service.get_bar(time, 5000)
                except:
                    continue
                self.data_service.push_data(data)
                super().dispatch('added', data)

                logging.info(self.data_service.get_count())
                if len(data) < 5000:
                    super().dispatch('tick', self.data_service.get_lasted_bar())
                import time
                time.sleep(5)

            except Exception:
                logging.error(traceback.format_exc())

# class Test(pycommon.patterns.Subscriber):
#     def __init__(self, name):
#         super().__init__(name)
#
#     def update(self, message):
#         print('{} got message "{}"'.format(self.name, message))
#
#
# s = Sync.default()
# s.register('tick', Test('test'))
# # s.register('added', test('added'))
# s.start()
