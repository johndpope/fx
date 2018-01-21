from .endpoint import endpoint
from ..request import Request


@endpoint(url='/candles/stream', method='GET', stream=True)
class StreamCandleRequest(Request):
    """
    client = API('http://172.104.110.189:9000')
    x = client.request(StreamCandleRequest())
    """

    def __init__(self):
        super(StreamCandleRequest, self).__init__()
