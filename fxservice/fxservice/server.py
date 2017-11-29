#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import cherrypy
import pycommon

from data_service_config import DataServiceConfig
from sync import start
from tick_store.influx_tick_store import InfluxTickStore

cfg = DataServiceConfig()

logger = pycommon.LogBuilder()
logger.init_rotating_file_handler(cfg.LogPath)
logger.init_stream_handler()
logger.build()

print(cfg)

db = InfluxTickStore.from_config()

start()


class Root:
    @cherrypy.expose
    def get_count(self):
        return str(db.get_count())

    @cherrypy.expose
    def get_current_value(self):
        return str(cr.get_account('101-011-6388580-001'))


cherrypy.tree.mount(Root(), '/', config={})

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
