from .endpoint import endpoint
from fxclient.fxclient.request import Request


@endpoint(url='/candles', method='GET', stream=True)
class GetCandlesRequest(Request):
    """
    client = API('http://172.104.110.189:9000')
    for v in client.request(GetDataRequest('2017-08-01T10:38:00Z', "2017-08-02T10:38:00Z")):
        logging.debug(v)
    """

    def __init__(self, start_time, end_time, chunk=4):
        super(GetCandlesRequest, self).__init__()
        super().add_query('start', start_time)
        super().add_query('end', end_time)
        super().add_query('chunk', chunk)
