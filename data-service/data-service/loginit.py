import logging
import os
from logging.handlers import RotatingFileHandler



def init():
    log_path = '/fx/logs'
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    debug_log = RotatingFileHandler(log_path + "/debug.log", maxBytes=5 * 1024 * 1024, mode='a', backupCount=10)
    debug_log.setLevel(logging.DEBUG)

    debug_log = RotatingFileHandler(log_path + "/info.log", maxBytes=5 * 1024 * 1024, mode='a', backupCount=10)
    debug_log.setLevel(logging.INFO)

    error_log = RotatingFileHandler(log_path + "/error.log", maxBytes=5 * 1024 * 1024, mode='a', backupCount=10)
    error_log.setLevel(logging.ERROR)


    handlers = [debug_log, error_log,  logging.StreamHandler()]
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=handlers)
