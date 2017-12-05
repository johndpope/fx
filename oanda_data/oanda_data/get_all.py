import sys

import pycommon

print(sys.path)

from oanda_broker_serivce.oanda_syn import OandaSync


class Test(pycommon.patterns.Subscriber):
    def __init__(self, name):
        super().__init__(name)

    def update(self, message):
        print('{} got message "{}"'.format(self.name, message))


s = OandaSync.default()
s.register('tick', Test('test'))
s.start()
