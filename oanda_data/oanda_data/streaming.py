import traceback

from oandapyV20 import API
from oandapyV20.endpoints.pricing import PricingStream

from oanda_data.oanda_data.config import Config

accountID = Config().AccountId
access_token = Config().OandaKey

api = API(access_token=access_token, environment="practice")

instruments = "EUR_USD"
s = PricingStream(accountID=accountID, params={"instruments": instruments})

for R in api.request(s):
    print(R)
    import requests

    try:

        url = Config().DataService + "/push_tick"
        import json

        payload = json.dumps(R)
        headers = {'content-type': 'application/json'}

        response = requests.request("POST", url, data=payload, headers=headers)
        print(json.loads(response.content))

    except:
        print(traceback.format_exc())
        pass
