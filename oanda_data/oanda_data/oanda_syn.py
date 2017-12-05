import datetime
import json
import logging
import traceback

import dateutil.parser
import pycommon
import requests
from config import Config
from oanda_broker_serivce.get_candle import CandleGetter
from oandapyV20 import API

cfg = Config()

logger = pycommon.LogBuilder()
logger.init_rotating_file_handler(cfg.LogPath)
logger.init_stream_handler()
logger.build()
logging.info('cfg:'+str(cfg))


class OandaSync:
    def __init__(self, get_data_function, get_lasted_function, push_function, batch_size):
        self.get_data_function = get_data_function
        self.get_lasted_function = get_lasted_function
        self.push_function = push_function
        self.batch = batch_size

    def start(self):
        time = self.get_lasted_function()
        while True:
            logging.debug('Get data')
            try:
                data = self.get_data_function(time, self.batch)
                print(len(data))
                if len(data) > 0:
                    self.push_function(data)
                    time = self.get_lasted_function()


            except Exception:
                logging.error(traceback.format_exc())


def get_lasted():
    try:
        import requests
        url = "http://localhost:9000/get_lasted_bar"
        response = requests.request("GET", url)
        obj = json.loads(response.text)
        logging.debug("get lasted: {}".format(obj['time']))
        time = obj['time']

        dt = dateutil.parser.parse(time)
        dt = dt + datetime.timedelta(seconds=60)
        dt = str(dt.isoformat())
        dt = dt.replace('+00:00', 'Z')
        logging.debug('lasted time:'+str(dt))
        return dt
    except:
        return '2000-01-01T00:00:00Z'


def push(data):
    url = Config().DataService + "/push_data"
    import json

    payload = json.dumps(data)
    headers = {'content-type': 'application/json'}

    response = requests.request("POST", url, data=payload, headers=headers)
    print(json.loads(response.content))


def get_data(time, count):
    cfg = Config()
    candle_getter = CandleGetter(api=API(access_token=cfg.OandaKey), accountID=cfg.AccountId)
    candle_getter.get_by_start_and_count(time, count)
    data = candle_getter.get_data()
    logging.debug("get data: len {}".format(len(data['candles'])))
    return data


s = OandaSync(get_data, get_lasted, push, cfg.BatchSize)
s.start()
