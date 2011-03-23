#!/usr/bin/env python
#-*- coding: utf8 -*-

from os.path import join, abspath, dirname

import tornado.web
import tornado.ioloop
from tornado.options import define, options, parse_config_file

from thumbor.handlers import MainHandler, HealthcheckHandler
from thumbor.utils import real_import


define('ENGINE',  default='thumbor.engines.pil')
define('LOADER',  default='thumbor.loaders.http_loader')
define('STORAGE', default='thumbor.storages.file_storage')
define('STORAGE_EXPIRATION_SECONDS', type=int, default=60 * 60 * 24 * 30) # default one month
define('MAGICKWAND_PATH', default=[])
define('FILTERS', default=['thumbor.filters.face_filter'], multiple=True)
define('FACE_FILTER_CASCADE_FILE', default='haarcascade_frontalface_alt.xml')


class ThumborServiceApp(tornado.web.Application):
    
    def __init__(self, conf_file=None):
        
        if conf_file is None:
            conf_file = abspath(join(dirname(__file__), 'conf.py'))
        parse_config_file(conf_file)

        loader = real_import(options.LOADER)
        storage = real_import(options.STORAGE)
        if hasattr(storage, 'init'):
            storage.init()
        engine = real_import(options.ENGINE).Engine()
        
        filters = []
        for filter_name in options.FILTERS:
            filters.append(real_import(filter_name).Filter())

        handlers = [
            (r'/healthcheck', HealthcheckHandler),
            (r'/(?:(\d+)x(\d+):(\d+)x(\d+)/)?(?:(-)?(\d+)?x(-)?(\d+)?/)?(?:(left|right|center)/)?(?:(top|bottom|middle)/)?(?:(smart)/)?(.+)', MainHandler, {
                'loader': loader,
                'storage': storage,
                'engine': engine,
                'filters': filters
            }),
        ]

        super(ThumborServiceApp, self).__init__(handlers)
