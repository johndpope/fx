import json


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
