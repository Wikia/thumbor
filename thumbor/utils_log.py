import logging
import logging.config

from pythonjsonlogger import jsonlogger
from datetime import datetime
from time import time

def configure_log(config, log_level):
    logger = logging.getLogger()
    logHandler = logging.StreamHandler()
    formatter = CustomJsonFormatter('(created) (name) (message) (funcName) (pathname) (filename) (lineno)')
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.setLevel(getattr(logging, log_level))

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        createdAt = log_record.get('created', time())
        log_record['timestamp'] = datetime.fromtimestamp(createdAt).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        log_record['appname'] = 'thumblr'
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

