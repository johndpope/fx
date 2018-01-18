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

    def from_dic(self, dic):
        super().from_dic(dic)
        super().merge_env()


cfg = Config()
print(cfg)
