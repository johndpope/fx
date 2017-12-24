import logging

import pycommon
from pycommon import ConfigBase
from pycommon import patterns


@patterns.singleton
class Config(ConfigBase):
    LogPath = '/tmp/logs'
    OandaKey = None
    AccountId = None
    DataService = None
    BatchSize = None


Config().merge_file(pycommon.get_callee_path() + "/config.ini")
Config().merge_env()
logging.debug(Config())
