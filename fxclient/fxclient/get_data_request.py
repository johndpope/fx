from fxclient.fxclient.endpoint import endpoint
from fxclient.fxclient.request import Request


@endpoint(url='get_data', method='GET', stream=False)
class GetDataRequest(Request):
    """
    client = API('http://172.104.110.189:9000')
    x = client.request(GetDataRequest('2017-08-01T10:38:00Z', "2017-08-02T10:38:00Z"))
    """

    def __init__(self, start_time, end_time):
        super(GetDataRequest, self).__init__()
        super().add_query('start', start_time)
        super().add_query('end', end_time)
