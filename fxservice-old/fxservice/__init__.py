import logging

from data_service_config import *

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger().setLevel(logging.INFO)

import pycommon

lb = pycommon.LogBuilder()

lb.init_rotating_file_stream_handler("/logs", pycommon.logging.ERROR)
lb.init_rotating_file_stream_handler("/logs", pycommon.logging.INFO)
lb.init_rotating_file_stream_handler("/logs", 100)
lb.init_stream_handler(pycommon.logging.DEBUG)
lb.init_stream_handler(100)
lb.build()
