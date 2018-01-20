#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os
import signal
import threading

import pycommon
import time
from client_streaming import ClientStreaming
from config import DataServiceConfig
from flask import Flask, request, jsonify, Response, stream_with_context
from kazoo.client import KazooClient
from tick_data_service.influx_tick_data_service import InfluxTickDataService

cfg = DataServiceConfig()
sleepEvent = threading.Event()


def disable_log():
    logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.ERROR)
    logging.getLogger("oandapyV20.oandapyV20").setLevel(logging.ERROR)
    logging.getLogger("kazoo.client").setLevel(logging.ERROR)


def init_zk_config():
    zk = KazooClient(hosts=os.environ['ZkServer'])
    zk.start()

    monitor_path = os.path.join(os.environ['ZkBasePath'], 'monitor/fxservice')
    zk.create(monitor_path, b'', ephemeral=True, makepath=True)

    @zk.DataWatch(os.path.join(os.environ['ZkBasePath'], "crawler"))
    def watch_node(data, stat):
        if sleepEvent.is_set():
            logging.warning("Restart fxservice")
            os.kill(os.getpid(), signal.SIGTERM)
        dic = json.loads(data.decode("utf-8"))
        cfg.from_dic(dic)
        sleepEvent.set()

    def heartbeat():
        while True:
            time.sleep(5)
            import datetime
            zk.set(monitor_path, str(datetime.datetime.now()).encode())
            # all of my code

    t = threading.Thread(target=heartbeat, args=())
    t.start()


def init_log():
    logger = pycommon.LogBuilder()
    logger.init_rotating_file_handler("/var/log/fxservice")
    logger.init_stream_handler()
    logger.build()
    logging.info('cfg:' + str(cfg))


disable_log()
init_zk_config()
init_log()

sleepEvent.wait()

db = InfluxTickDataService.from_config()
app = Flask(__name__)


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
