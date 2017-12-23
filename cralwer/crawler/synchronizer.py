import datetime
import json
import logging
import traceback

import dateutil.parser
import pycommon
from config import Config
from fxclient.fxclient.endpoints.get_lasted_candle_request import GetLastedCandlesRequest
from fxclient.fxclient.api import FxAPI
from fxclient.fxclient.endpoints.post_candles import PostCandlesRequest
from oandapyV20 import API

from cralwer.crawler.oanda.downloader import Downloader

cfg = Config()

logging.getLogger("urllib3").setLevel(logging.ERROR)

logger = pycommon.LogBuilder()
logger.init_rotating_file_handler(cfg.LogPath)
logger.init_stream_handler()
logger.build()
logging.info('cfg:' + str(cfg))


class OandaSync:
    def __init__(self, get_data_function, get_lasted_function, push_function, batch_size):
        self.get_data_function = get_data_function
        self.get_lasted_function = get_lasted_function
        self.push_function = push_function
        self.batch = batch_size

    def start(self):
        lasted_time = self.get_lasted_function()
        while True:
            logging.debug('Get data')
            try:
                data = self.get_data_function(lasted_time, self.batch)
                print(len(data['candles']))
                if len(data['candles']) > 0:
                    self.push_function(data)
                    lasted_time = self.get_lasted_function()
                    print(lasted_time)
                else:
                    import time
                    time.sleep(30)
            except Exception:
                logging.error(traceback.format_exc())
                import time
                time.sleep(30)


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
        print(traceback.format_exc())
        return '2017-01-01T00:00:00Z'


def push(data):
    url = cfg.DataService
    api = FxAPI(url)
    response = api.request(PostCandlesRequest(data))
    print(response)


def get_data(time, count):
    candle_getter = Downloader(api=API(access_token=cfg.OandaKey), accountID=cfg.AccountId)
    candle_getter.get_by_start_and_count(time, count)
    data = candle_getter.get_data()
    logging.debug("get data: len {}".format(len(data['candles'])))
    return data


s = OandaSync(get_data, get_lasted, push, cfg.BatchSize)
s.start()
