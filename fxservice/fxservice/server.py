#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import logging
import queue

import pycommon
from config import DataServiceConfig
from flask import Flask, request, jsonify, Response, stream_with_context
from stream import CandleFactory, StreamRecord
from tick_data_service.influx_tick_data_service import InfluxTickDataService

app = Flask(__name__)
cfg = DataServiceConfig()
logger = pycommon.LogBuilder()
logger.init_rotating_file_handler(cfg.LogPath)
logger.init_stream_handler()
logger.build()

print(cfg)

db = InfluxTickDataService.from_config()


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


@app.route('/')
def hello_world():
    return 'Hello from data service !'


@app.route('/push_data', methods=['POST'])
def push_data():
    data_obj = json.loads(request.data)

    logging.debug("added len: {}".format(len(data_obj)))
    db.push_data(data_obj)
    return jsonify({"added": len(data_obj['candles'])})


candle_factory = CandleFactory("EUR_USD", "M1")


@app.route('/push_tick', methods=['POST'])
def push_tick():
    data_obj = json.loads(request.data)
    if data_obj['type'] != 'PRICE':
        return jsonify({"status": "success"})

    print(data_obj)

    new_obj = {"tick": {"ask": data_obj['asks'][0]['price'], "instrument": data_obj['instrument'],
                        "bid": data_obj['bids'][0]['price'],
                        "time": data_obj['time']}}

    r = candle_factory.processTick(StreamRecord(new_obj))

    #
    # if r is not None:
    #     db.push_data(
    #     {
    #         'closeAsk': 1,
    #         'closeBid': 2,
    #
    #         'highAsk': 3,
    #         'highBid': 3,
    #
    #         'lowAsk': 4,
    #         'lowBid': 5,
    #
    #         'openAsk': 6,
    #         'openBid': 6,
    #
    #         'volume': 6,
    #         # 'time':
    #     })

    return jsonify({"status": "success"})

    # logging.debug("added len: {}".format(len(data_obj)))
    # db.push_data(data_obj)
    # return jsonify({"added": len(data_obj)})


@app.route('/data_stream')
def data_stream():
    client = ClientStreaming()
    db.register('added', client)

    return Response(stream_with_context(client.start()), mimetype='text/event-stream')


@app.route('/get_data_stream')
def get_data_stream():
    start = request.args.get('start')
    end = request.args.get('end')
    chunk = int(request.args.get('chunk', 1))

    def generate():
        data = db.get_bars(start, end)
        arr = []
        for item in data:
            arr.append(item)
            if len(arr) == chunk:
                byte_data = (json.dumps(arr) + "\n").encode()
                yield byte_data
                arr.clear()
        if len(arr) > 0:
            byte_data = (json.dumps(arr) + "\n").encode()
            yield byte_data

    return Response(stream_with_context(generate()), mimetype='text/event-stream')


@app.route('/get_lasted_bar')
def get_lasted_bar():
    lasted = db.get_lasted_bar()
    if lasted is None:
        return jsonify({})
    return jsonify(lasted)


@app.route('/get_count')
def get_count():
    data = db.get_count()
    return Response(json.dumps({"count": data}), mimetype='application/json')


@app.route('/get_data')
def get_data():
    start = request.args.get('start')
    end = request.args.get('end')
    print(start, end)
    data = db.get_bars(start, end)
    return Response(json.dumps(data), mimetype='application/json')


if __name__ == '__main__':
    app.run(threaded=True, port=9000, host='0.0.0.0')
