import logging
import traceback

import pycommon

#
from crawl_service.oanda_service import OandaCrawl
from tick_store.influx_tick_store import InfluxTickStore

lb = pycommon.LogBuilder()

lb.init_rotating_file_stream_handler("/logs", logging.ERROR)
lb.init_rotating_file_stream_handler("/logs", logging.INFO)
lb.init_rotating_file_stream_handler("/logs", 100)
lb.init_stream_handler(logging.DEBUG)
lb.init_stream_handler(100)
lb.build()

logging.getLogger("urllib3").setLevel(logging.WARNING)

import threading

db = InfluxTickStore.from_config()
crawler = OandaCrawl.from_config()


def start():
    threading.Timer(60, start).start()
    logging.debug('Get data')
    try:
        time = db.get_lasted_bar({'time': '2000-01-01'})['time']
        data = crawler.get(time, 5000)
        db.push_data(data)
        logging.log(100, "Success:" + time + " " + str(len(data)))
        if len(data) == 1:
            print(data)
    except Exception:
        logging.error(traceback.format_exc())


start()
