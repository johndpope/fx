import importlib
import logging
import os
import re
import sys
import tempfile
import zipfile

import backtrader as bt
import pycommon
from kazoo.client import KazooClient
from test_data_source import TestDataSource

if 'ZkServer' not in os.environ or 'ZkBasePath' not in os.environ:
    os.environ['ZkServer'] = '172.104.110.189:2181'
    os.environ['ZkBasePath'] = 'fx.dev'

zk = KazooClient(hosts=os.environ['ZkServer'])
zk.start()
monitor_path = os.path.join(os.environ['ZkBasePath'], "tasks")

logging.getLogger("kazoo.client").setLevel(logging.ERROR)


def init_log():
    logger = pycommon.LogBuilder()
    logger.init_stream_handler(level=logging.INFO)
    logger.build()


def run_stategy(strategy_zip_file):
    zip_ref = zipfile.ZipFile(strategy_zip_file, 'r')
    folder = tempfile.mkdtemp()
    zip_ref.extractall(folder)
    zip_ref.close()
    sys.path.append(folder)

    def form_module(fp):
        return '.' + os.path.splitext(fp)[0]

    def load_plugins():
        py_search_re = re.compile('^' + 'strategy' + '.py$', re.IGNORECASE)
        plugin_files = list(filter(py_search_re.search, os.listdir(folder + "/strategy")))
        plugins = list(map(form_module, plugin_files))
        importlib.import_module('strategy')
        modules = []
        for plugin in plugins:
            if not plugin.startswith('__'):
                m = importlib.import_module(plugin, package='strategy')
                modules.append(m)
                importlib.reload(m)

        return modules

    m = load_plugins()[0]

    cerebro = bt.Cerebro()
    cerebro.addstrategy(m.getStrategy())
    data = TestDataSource('2017-01-01T10:38:00Z', "2017-01-30T10:38:00Z")
    cerebro.adddata(data)
    cerebro.broker.setcash(2000)

    cerebro.run()

    pycommon.logging.debug('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    return cerebro.broker.getvalue()
    # cerebro.plot()


init_log()
import os


def process_node(path, new_worker, data):
    pycommon.logging.info("Working {} on process {}:".format(work_node, os.getpid()))

    file = tempfile.mktemp()
    with open(file, 'wb') as f:
        f.write(data)
    value = run_stategy(file)
    result = os.path.join(path, 'result')
    zk.create(result, str(value).encode(), ephemeral=False)
    zk.delete(new_worker)


while True:
    monitor_path = os.path.join(os.environ['ZkBasePath'], "tasks")
    lock = zk.Lock(os.path.join(os.environ['ZkBasePath'], "lock"), "worker")
    work_node, worker_node = None, None
    with lock:  # blocks waiting for lock acquisition
        children = zk.get_children(monitor_path)
        for v in children:
            worker = zk.get_children(os.path.join(monitor_path, v))
            if len(worker) == 0:  # execute worker
                new_worker = zk.create(os.path.join(monitor_path, v, str(os.getpid())), ephemeral=True)
                work_node = os.path.join(monitor_path, v)
                worker_node = new_worker
                break
        import time
    if not work_node:
        time.sleep(5)
        pycommon.logging.info("No task found")
    if work_node:
        data, start = zk.get(work_node)
        process_node(work_node, new_worker, data)
