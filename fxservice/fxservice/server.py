#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging

import pycommon
from client_streaming import ClientStreaming
from config import DataServiceConfig
from flask import Flask, request, jsonify, Response, stream_with_context
from tick_data_service.influx_tick_data_service import InfluxTickDataService

app = Flask(__name__)
cfg = DataServiceConfig()
logger = pycommon.LogBuilder()
logger.init_rotating_file_handler(cfg.LogPath)
logger.init_stream_handler()
logger.build()

logging.debug(cfg)

db = InfluxTickDataService.from_config()


@app.route('/')
def hello_world():
    return 'Hello from data service !'


@app.route('/candles', methods=['POST'])
def post_candles():
    data_obj = json.loads(request.data)
    logging.debug("added len: {}".format(len(data_obj)))
    db.push_data(data_obj)
    return jsonify({"added": len(data_obj['candles'])})


@app.route('/candles/stream', methods=['GET'])
def stream_candle():
    logging.debug("Stream")
    client = ClientStreaming()
    db.register('added', client)
    return Response(stream_with_context(client.start()), mimetype='text/event-stream')


@app.route('/candles/lasted', methods=['GET'])
def get_candles_lasted():
    lasted = db.get_lasted_bar()
    if lasted is None:
        return jsonify({})
    return jsonify(lasted)


@app.route('/candles/count', methods=['GET'])
def get_candles_count():
    data = db.get_count()
    return Response(json.dumps({"count": data}), mimetype='application/json')


@app.route('/candles', methods=['GET'])
def get_candles():
    start = request.args.get('start')
    end = request.args.get('end')
    chunk = int(request.args.get('chunk', 1))

    logging.debug("Get candles from {} to {} chunk {}".format(start, end, chunk))

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


if __name__ == '__main__':
    app.run(threaded=True, port=9000, host='0.0.0.0')
