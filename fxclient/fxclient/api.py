import json

import requests


class Request:
    def __init__(self):
        self.headers = {'content-type': 'application/json'}
        self.body = ''
        self.query = {}

    def add_query(self, key, value):
        self.query[key] = value

    def add_header(self, key, value):
        self.headers[key] = value

    def add_header(self, key, value):
        self.headers[key] = value

    def set_body(self, value):
        if value is str:
            self.body = value
        elif value is dict:
            self.body = json.dumps(value)
        else:
            raise Exception("Unknown body")


def end_point(url, method="GET", stream=False):
    def dec(obj):
        obj.endpoint = url
        obj.method = method
        obj.stream = stream
        return obj

    return dec


@end_point(url='get_data', method='GET', stream=False)
class GetDataRequest(Request):
    def __init__(self, start_time, end_time):
        super(GetDataRequest, self).__init__()
        super().add_query('start', start_time)
        super().add_query('end', end_time)


@end_point(url='get_data_stream', method='GET', stream=True)
class GetDataStreamRequest(Request):
    def __init__(self, start_time, end_time, chunk=4):
        super(GetDataStreamRequest, self).__init__()
        super().add_query('start', start_time)
        super().add_query('end', end_time)
        super().add_query('chunk', chunk)
        pass


class API:
    def __init__(self, service):
        self.service = service

    def __stream_request(self, response):
        lines = response.iter_lines()
        for line in lines:
            if line:
                data = json.loads(line.decode("utf-8"))
                yield data

    def request(self, request):
        url = self.service + "/" + request.endpoint

        if not request.stream:
            response = requests.request(request.method, url, data=request.body, headers=request.headers,
                                        params=request.query)
            obj = json.loads(response.text)
            return obj
        else:
            response = requests.request(request.method, url, data=request.body, headers=request.headers,
                                        params=request.query, stream=True)
            return self.__stream_request(response)


client = API('http://172.104.110.189:9000')
# x = client.request(GetDataRequest('2017-08-01T10:38:00Z', "2017-08-02T10:38:00Z"))
# print(x)
for v in client.request(GetDataStreamRequest('2017-08-01T10:38:00Z', "2017-08-02T10:38:00Z")):
    print(v)
