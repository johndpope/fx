import base64
import importlib
import logging
import os
import re
import sys
import tempfile
import time
import zipfile

import backtrader as bt
import pycommon
from fxclient.data.test_data_source_list import TestDataSourceList
from kazoo.client import KazooClient

from storage import MongoDatabase


def init_default():
    """
    Đặt các biến môi trường mặc định
    :return:
    """
    if 'ZkServer' not in os.environ:
        os.environ['ZkServer'] = '172.104.110.189:2181'

    if 'ZkBasePath' not in os.environ:
        os.environ['ZkBasePath'] = 'fx.dev1'





def init_log():
    """
    Init log
    :return:
    """
    logging.getLogger("kazoo.client").setLevel(logging.ERROR)

    logger = pycommon.LogBuilder()
    logger.init_stream_handler(level=logging.INFO)
    logger.build()


def run_strategy(strategy_zip_file):
    """
    Chạy 1 strategy ở dạng zip file
    :param strategy_zip_file:
    """
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
    # data = TestDataSource('2017-01-01T10:38:00Z', "2017-01-30T10:38:00Z")
    data = TestDataSourceList('2017-01-01T10:38:00Z', "2017-01-05T10:38:00Z")

    cerebro.adddata(data)
    cerebro.broker.setcash(2000)

    cerebro.run()

    return cerebro.broker.getvalue()


def save_to_db(function, zip):
    result = function(zip)
    storage_data = MongoDatabase()
    with open(zip, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        storage_data.save_item({"zip_file": encoded_string, "total_value": str(result)})

    # print(zip + " " + str(result))


def process_node(path, new_worker, data):
    """
    Xử lý một node
    :param path: Đường dẫn node cần xử lý
    :param new_worker: Tên workder xử lý
    :param data: Dữ liệu dạng zip
    :return:
    """
    logging.info("Working {} on process {}:".format(new_worker, os.getpid()))

    file = tempfile.mktemp()
    with open(file, 'wb') as f:
        f.write(data)
    save_to_db(run_strategy, file)
    # result = os.path.join(path, 'result')
    # zk.create(result, str(value).encode(), ephemeral=False)
    zk.delete(path, recursive=True)


def main():
    """
    Vòng lặp vô hạn để luôn kiểm tra và thực thi task nếu có
    :return:
    """
    while True:
        tasks_path = os.path.join(os.environ['ZkBasePath'], "tasks")
        lock = zk.Lock(os.path.join(os.environ['ZkBasePath'], "lock"), "worker")
        working_node, worker_node = None, None
        with lock:  # blocks waiting for lock acquisition
            children = zk.get_children(tasks_path)
            for v in children:
                try:
                    worker = zk.get_children(os.path.join(tasks_path, v))
                    if len(worker) == 0:  # execute worker
                        worker_node = zk.create(os.path.join(tasks_path, v, str(os.getpid())), ephemeral=True)
                        working_node = os.path.join(tasks_path, v)
                        break
                except:
                    pass

        if not working_node:
            time.sleep(5)
            pycommon.logging.info("No task found")
        else:
            data, start = zk.get(working_node)
            process_node(working_node, worker_node, data)


if __name__ == "__main__":
    init_log()
    init_default()
    # logging.info(save_to_db(run_strategy, '/opt/projects/fx/strategy/strategy/strategy.zip'))
    #
    # exit()
    zk = KazooClient(hosts=os.environ['ZkServer'])
    zk.start()

    main()
