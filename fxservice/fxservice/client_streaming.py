import json
import queue

import pycommon.patterns


class ClientStreaming(pycommon.patterns.Subscriber):
    def __init__(self):
        self.q = queue.Queue()
        self.name = 'Streaming client'
        print('Streaming client registered')

    def update(self, message):
        print('{} got message "{}"'.format(self.name, message))
        self.q.put(message)

    def start(self):
        while True:
            data = self.q.get()
            byte_data = (json.dumps(data) + "\n").encode()
            yield byte_data