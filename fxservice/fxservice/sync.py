import logging
import traceback

from broker_service.oanda_broker_service import OandaBrokerService
from tick_data_service.influx_tick_data_service import InfluxTickDataService

logging.getLogger().setLevel(logging.INFO)

db = InfluxTickDataService.from_config()
crawler = OandaBrokerService.from_config()


def start():
    while True:
        logging.debug('Get data')
        try:
            time = db.get_lasted_bar({'time': '2000-01-01'})['time']
            try:
                data = crawler.get_bar(time, 5000)
            except:
                continue
            db.push_data(data)

            logging.info(db.get_count())
            if len(data) < 5000:
                logging.info(db.get_lasted_bar())

        except Exception:
            logging.error(traceback.format_exc())


start()
