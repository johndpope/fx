#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import logging

import pycommon
from flask import Flask, request, jsonify, Response, stream_with_context

from data_service_config import DataServiceConfig
from fxservice.fxservice.tick_data_service.influx_tick_data_service import InfluxTickDataService

app = Flask(__name__)
cfg = DataServiceConfig()
logger = pycommon.LogBuilder()
logger.init_rotating_file_handler(cfg.LogPath)
logger.init_stream_handler()
logger.build()

print(cfg)

db = InfluxTickDataService.from_config()


@app.route('/')
def hello_world():
    return 'Hello from data service !'


@app.route('/get_data_stream')
def get_data_stream():
    start = request.args.get('start')
    end = request.args.get('end')

    def generate():
        data = db.get_bars(start, end)
        for item in data:
            byte_data = json.dumps(item).encode()
            yield byte_data

    return Response(stream_with_context(generate()), mimetype='application/json')


@app.route('/get_data')
def get_data():
    start = request.args.get('start')
    end = request.args.get('end')
    print(start, end)
    data = db.get_bars(start, end)
    return Response(json.dumps(data), mimetype='application/json')


@app.route('/push_data', methods=['GET', 'POST'])
def push_data():
    data_obj = json.loads(request.data)
    converted = []

    for v in data_obj:
        converted.append({
            "measurement": "ticks",
            "time": v['time'],
            "fields": {
                'closeAsk': v['closeAsk'],
                'closeBid': v['closeBid'],
                'highAsk': v['highAsk'],
                'highBid': v['highBid'],
                'lowAsk': v['lowAsk'],
                'lowBid': v['lowBid'],
                'openAsk': v['openAsk'],
                'openBid': v['openBid'],
                'volume': v['volume'],
                'time': v['time']
            }
        })
    print(converted[0]['fields']['time'])
    logging.debug("added len: {}".format(len(data_obj)))
    db.push_data(converted)
    return jsonify({"added": len(data_obj)})


if __name__ == '__main__':
    app.run(threaded=True)
