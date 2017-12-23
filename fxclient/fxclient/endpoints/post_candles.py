from ..request import Request

from .endpoint import endpoint


@endpoint(url='/candles', method='POST')
class PostCandlesRequest(Request):

    def __init__(self, data):
        super(PostCandlesRequest, self).__init__()
        super().set_body(data)
