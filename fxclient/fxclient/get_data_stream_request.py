from fxclient.fxclient.endpoint import endpoint
from fxclient.fxclient.request import Request


@endpoint(url='get_data_stream', method='GET', stream=True)
class GetDataStreamRequest(Request):
    """
    client = API('http://172.104.110.189:9000')
    for v in client.request(GetDataStreamRequest('2017-08-01T10:38:00Z', "2017-08-02T10:38:00Z")):
        print(v)
    """

    def __init__(self, start_time, end_time, chunk=4):
        super(GetDataStreamRequest, self).__init__()
        super().add_query('start', start_time)
        super().add_query('end', end_time)
        super().add_query('chunk', chunk)
        pass
