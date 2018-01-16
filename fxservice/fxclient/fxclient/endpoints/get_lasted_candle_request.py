from .endpoint import endpoint
from ..request import Request


@endpoint(url='/candles/lasted', method='GET')
class GetLastedCandlesRequest(Request):

    def __init__(self):
        super(GetLastedCandlesRequest, self).__init__()
