import json
import logging
import queue

import pycommon.patterns


class ClientStreaming(pycommon.patterns.Subscriber):
    def __init__(self):
        self.q = queue.Queue()
        self.name = 'Streaming client'
        logging.debug('Streaming client registered')

    def update(self, message):
        # logging.debug('{} got message "{}"'.format(self.name, message))
        self.q.put(message)

    def start(self):
        while True:
            data = self.q.get()
            byte_data = (json.dumps(data) + "\n").encode()
            yield byte_data
