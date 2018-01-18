import pycommon
from pycommon import ConfigBase
from pycommon import patterns


@patterns.singleton
class DataServiceConfig(ConfigBase):
    DbHost = None
    DbPort = None
    DbUser = None
    DbPass = None
    DbName = None


config = DataServiceConfig()
print(config)
