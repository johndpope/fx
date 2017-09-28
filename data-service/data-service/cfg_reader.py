import configparser
import os
import sys

config = None

 
def __init(file_path):
    global config
    config = configparser.ConfigParser()
    config.read(file_path)


def get_config(key, default_value=None, session='DEFAULT'):
    if config is None:
        __init(os.path.dirname(os.path.realpath(sys.argv[0])) + "/config.ini")

    session = config[session]
    if key in os.environ:
        return os.environ[key]

    value = session.get(key, None)
    if value is None:
        return default_value
    return value
