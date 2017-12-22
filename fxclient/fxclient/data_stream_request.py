from fxclient.fxclient.endpoint import endpoint
from fxclient.fxclient.request import Request


@endpoint(url='data_stream', method='GET', stream=True)
class StreamDataRequest(Request):
    """
    client = API('http://172.104.110.189:9000')
    x = client.request(GetDataRequest('2017-08-01T10:38:00Z', "2017-08-02T10:38:00Z"))
    """

    def __init__(self):
        super(StreamDataRequest, self).__init__()
