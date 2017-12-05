from oandaV20 import api
from oanda_data.oanda_data.config import Config


"""
Create an API context, and use it to fetch candles for an instrument.
The configuration for the context is parsed from the config file provided
as an argumentV
"""

instrument = 'EUR_USD'
mid = False
bid = False
ask = False
granularite = 'M1'
count = 10
date_format = "%Y-%m-%d %H:%M:%S"

account_id = Config().AccountId
price = "mid"

response = api.instrument.candles("EUR_USD", account_id=account_id,)

print(response)

print("Instrument: {}".format(response.get("instrument", 200)))
print("Granularity: {}".forzzmat(response.get("granularity", 200)))
