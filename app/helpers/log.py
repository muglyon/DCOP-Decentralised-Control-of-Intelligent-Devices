import logging
import json
from pythonjsonlogger import jsonlogger

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
FORMAT_STR = '{"asctime": %(asctime)s, ' \
             '"topic": "%(topic)s", ' \
             '"type": "%(type)s", ' \
             '"content": %(message)s, ' \
             '"level": "%(levelname)s"}'


def setup_custom_logger(file_name):
    logging.basicConfig(format=FORMAT_STR, filename=file_name, level=logging.INFO, datefmt=DATE_FORMAT)

    handler = logging.StreamHandler()
    handler.setFormatter(jsonlogger.JsonFormatter(FORMAT_STR))

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def info(msg, id, type):
    prefix = "" if "DCOP/" in str(id) else "DCOP/"
    logging.getLogger().info(json.dumps(msg), extra={'topic': prefix + str(id), 'type': type})

