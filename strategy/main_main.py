import importlib
import re
import sys
import zipfile

import backtrader as bt
import pycommon
from gevent import os
from test_data_source import TestDataSource

zip_ref = zipfile.ZipFile('strategy.zip', 'r')
import tempfile

folder = tempfile.mkdtemp()
zip_ref.extractall(folder)
zip_ref.close()

sys.path.append(folder)


def init_log():
    logger = pycommon.LogBuilder()
    logger.init_rotating_file_handler("/var/log/fxservice")
    logger.init_stream_handler()
    logger.build()


init_log()


def load_plugins():
    py_search_re = re.compile('^' + 'strategy' + '.py$', re.IGNORECASE)
    plugin_files = filter(py_search_re.search, os.listdir(folder + "/strategy"))
    form_module = lambda fp: '.' + os.path.splitext(fp)[0]
    plugins = list(map(form_module, plugin_files))
    # import parent module namespace
    importlib.import_module('strategy')
    modules = []
    for plugin in plugins:
        if not plugin.startswith('__'):
            m = importlib.import_module(plugin, package='strategy')
            modules.append(m)
            importlib.reload(m)

    return modules


m = load_plugins()[0]

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(m.getStrategy())
    data = TestDataSource('2017-01-01T10:38:00Z', "2017-01-30T10:38:00Z")
    # data = LiveDataSource()
    cerebro.adddata(data)
    cerebro.broker.setcash(2000)
    from matplotlib.dates import *

    cerebro.run()

    pycommon.logging.debug('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()

print(folder)
