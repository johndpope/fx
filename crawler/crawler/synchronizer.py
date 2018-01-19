import datetime
import json
import logging
import os
import signal
import threading
import traceback

import dateutil.parser
import pycommon
from config import Config
from fxclient.endpoints.get_lasted_candle_request import GetLastedCandlesRequest
from fxclient.endpoints.post_candles import PostCandlesRequest
from fxclient.fxapi import FxAPI
from kazoo.client import KazooClient
from oanda.downloader import Downloader
from oandapyV20 import API
import time

logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.ERROR)
logging.getLogger("oandapyV20.oandapyV20").setLevel(logging.ERROR)

cfg = Config()

config_path = os.path.join(os.environ['ConfigBasePath'], "crawler")
zk = KazooClient(hosts=os.environ['ConfigServer'])
zk.start()
zk.ensure_path(config_path)

monitor_path = os.path.join(os.environ['ConfigBasePath'], 'monitor/crawler')
zk.create(monitor_path, b'', ephemeral=True, makepath=True)

sleepEvent = threading.Event()


@zk.DataWatch(config_path)
def watch_node(data, stat):
    if sleepEvent.is_set():
        logging.warning("Restart fxservice")
        os.kill(os.getpid(), signal.SIGTERM)
    dic = json.loads(data.decode("utf-8"))
    cfg.from_dic(dic)
    sleepEvent.set()


sleepEvent.wait()

logger = pycommon.LogBuilder()
logger.init_rotating_file_handler(cfg.LogPath)
logger.init_stream_handler()
logger.build()
logging.info('cfg:' + str(cfg))


class OandaSync:
    def __init__(self, get_data_function, get_lasted_function, push_function, batch_size, delay_time):
        self.delay_time = delay_time
        self.get_data_function = get_data_function
        self.get_lasted_function = get_lasted_function
        self.push_function = push_function
        self.batch = batch_size

    def start(self):
        lasted_time = self.get_lasted_function()
        while True:
            logging.debug('Get data')

            if self.delay_time != 0:
                time.sleep(self.delay_time)
            try:
                data = self.get_data_function(lasted_time, self.batch)
                logging.debug(len(data['candles']))
                if len(data['candles']) > 0:
                    self.push_function(data)
                    lasted_time = self.get_lasted_function()
                    logging.debug(lasted_time)
                else:
                    time.sleep(30)
            except Exception:
                logging.error(traceback.format_exc())
                time.sleep(5)


def get_lasted():
    try:

        url = cfg.DataService
        api = FxAPI(url)
        response = api.request(GetLastedCandlesRequest())
        time = response['time']

        dt = dateutil.parser.parse(time)
        dt = dt + datetime.timedelta(seconds=60)
        dt = str(dt.isoformat())
        dt = dt.replace('+00:00', 'Z')
        logging.debug('lasted time:' + str(dt))
        return dt
    except:
        logging.error(traceback.format_exc())
        return '2010-01-01T00:00:00Z'


def push(data):
    url = cfg.DataService
    api = FxAPI(url)
    response = api.request(PostCandlesRequest(data))
    logging.debug(response)


def get_data(time, count):
    candle_getter = Downloader(api=API(access_token=cfg.OandaKey), accountID=cfg.AccountId)
    candle_getter.get_by_start_and_count(time, count)
    data = candle_getter.get_data()
    logging.debug("get data: len {}".format(len(data['candles'])))
    return data


s = OandaSync(get_data, get_lasted, push, cfg.BatchSize, cfg.DelayTime)
s.start()
