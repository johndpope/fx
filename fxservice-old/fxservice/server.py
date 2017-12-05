#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import cherrypy
import pycommon
from data_service_config import DataServiceConfig

from fxservice.fxservice.broker_service import OandaBrokerService
from fxservice.fxservice.tick_data_service.influx_tick_data_service import InfluxTickDataService

cfg = DataServiceConfig()

logger = pycommon.LogBuilder()
logger.init_rotating_file_handler(cfg.LogPath)
logger.init_stream_handler()
logger.build()

print(cfg)

db = InfluxTickDataService.from_config()
br = OandaBrokerService.from_config()


def make_response_json(method):
    def method_make(*args, **kw):
        import cherrypy
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'X-Requested-With'
        cherrypy.response.headers['Content-Type'] = "application/json"
        return method(*args, **kw)

    return method_make


class Account:
    @cherrypy.expose
    def get_profit_loss(self):
        return str(br.get_profit_loss('101-011-6388580-001'))


class Root:
    def index(self):
        return "Hello, world!"

    index.exposed = True


class Data:
    @cherrypy.expose
    @make_response_json
    def get_bar(self, start, end):
        return str(db.get_lasted_bar(start, end))

    @cherrypy.expose
    @make_response_json
    def get_count(self):
        return str(db.get_count())

    @cherrypy.expose
    @make_response_json
    def get_last_bar(self):
        return str(db.get_lasted_bar())


cherrypy.tree.mount(Root(), '/', config={})
cherrypy.tree.mount(Data(), '/data/', config={})
cherrypy.tree.mount(Account(), '/account/', config={})

config = {
    'tools.staticdir.debug': True,
    'log.screen': True,
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 9000,
    'tools.sessions.on': True,
    'tools.encode.on': True,
    'tools.encode.encoding': 'utf-8',
    'server.thread_pool': 30,
    'tools.encode.text_only': False,
    'engine.autoreload.on': False
}
cherrypy.config.update(config)
cherrypy.engine.start()
