import json

import requests


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

#
# client = API('http://172.104.110.189:9000')
# # x = client.request(GetDataRequest('2017-08-01T10:38:00Z', "2017-08-02T10:38:00Z"))
# # print(x)
# for v in client.request(GetDataStreamRequest('2017-08-01T10:38:00Z', "2017-08-02T10:38:00Z")):
#     print(v)
