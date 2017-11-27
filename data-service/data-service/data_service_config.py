import pycommon
from pycommon import ConfigBase
from pycommon import patterns


@patterns.singleton
class DataServiceConfig(ConfigBase):
    LogPath = '/tmp/logs'
    OandaKey = None
    DbHost = None
    DbPort = None
    DbUser = None
    DbPass = None


DataServiceConfig().merge_file(pycommon.get_callee_path() + "/config.ini")
