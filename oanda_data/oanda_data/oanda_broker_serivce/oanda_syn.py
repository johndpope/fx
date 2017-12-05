import logging
import traceback

import pycommon

from oanda_broker_service import OandaBrokerService


class OandaSync(pycommon.patterns.Publisher):
    @classmethod
    def default(cls):
        broker_service = OandaBrokerService.from_config()
        return OandaSync(broker_service)

    def __init__(self, broker_service):
        super(OandaSync, self).__init__(['tick', 'added'])
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
