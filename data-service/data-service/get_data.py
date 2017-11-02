import logging
import traceback

import pycommon

import fx_data_service
from odana_service import OdanaClient

pycommon.init_rotating_file("/fx/logs/")
logging.getLogger("urllib3").setLevel(logging.WARNING)

odana = OdanaClient(pycommon.get_env_or_config('odanakey'))
fx_service = fx_data_service.FxDataService(pycommon.get_env_or_config('host'),
                                           pycommon.get_env_or_config('port'))

print(pycommon.get_env_or_config('host'))
print(pycommon.get_env_or_config('port'))

while True:
    try:

        time = fx_service.get_lasted_bar({'time':'2000-01-01'})['time']
        data = odana.get_from_odana(time, 5000)
        fx_service.push_data(data)

        logging.info("Success:" + time + " " + str(len(data)))
    except:
        logging.error(traceback.format_exc())
