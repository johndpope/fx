from oandapyV20 import API
from oandapyV20.endpoints.accounts import AccountSummary

accountID = "101-011-6388580-001"
access_token = "0cd4c62c9ea093e77c2086fcc61053ed-19807c1fb8c8e289298d7f9ae3351a72"

api = API(access_token=access_token, environment="practice")

instruments = "EUR_USD"

# EUR_USD (today 1.0750)
EUR_USD_STOP_LOSS = 1.07
EUR_USD_TAKE_PROFIT = 1.10

while True:
    r = AccountSummary(accountID)
    re=api.request(r)
    print(re['account']['unrealizedPL'])
    import time
    time.sleep(0)
exit()

r = trades.OpenTrades(accountID)
rv = api.request(r)
print(rv)

mktOrder = MarketOrderRequest(
    instrument="EUR_USD",
    units=10)

# create the OrderCreate request
r = orders.OrderCreate(accountID, data=mktOrder.data)
try:
    # create the OrderCreate request
    rv = api.request(r)
except oandapyV20.exceptions.V20Error as err:
    print(r.status_code, err)
else:
    print(json.dumps(rv, indent=2))

r = orders.OrderCreate(accountID, data=mktOrder.data)
# perform the request
rv = api.request(r)
print(rv)
print(json.dumps(rv, indent=4))
# s = PricingStream(accountID=accountID, params={"instruments": instruments})
# try:
#     n = 0
#     for R in api.request(s):
#         if R['type'] != 'PRICE':
#             continue
#         print(R['bids'][0]['price'])
#
#         n += 1
#         if n > 1000:
#             s.terminate("maxrecs received: {}")
#
# except V20Error as e:
#     print("Error: {}".format(e))
