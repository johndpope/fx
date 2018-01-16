from fxapi import FxAPI
from stream_candle_request import StreamCandleRequest
from .strategy import *

client = FxAPI('http://172.104.110.189:9000')
generator = client.request(StreamCandleRequest())
for v in generator:
    print(v)