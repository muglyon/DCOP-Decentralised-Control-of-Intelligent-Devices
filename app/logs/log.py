import logging
import json

from pythonjsonlogger import jsonlogger
from logs import elasticsearch

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
FORMAT_STR = '{"asctime": "%(asctime)s", ' \
             '"topic": "%(topic)s", ' \
             '"type": "%(type)s", ' \
             '"content": %(message)s, ' \
             '"level": "%(levelname)s"}'


def setup_custom_logger(file_name):

    logging.basicConfig(format=FORMAT_STR,
                        filename=file_name,
                        level=logging.INFO,
                        datefmt=DATE_FORMAT)

    handler_log = logging.StreamHandler()
    handler_log.setFormatter(jsonlogger.JsonFormatter(FORMAT_STR))

    logger = logging.getLogger()
    logger.addHandler(handler_log)
    logger.propagate = False

    return logger


def info(msg, sender_id, msg_type):

    logger = logging.getLogger()
    prefix = "" if "DCOP/" in str(sender_id) else "DCOP/"
    payload = json.dumps(msg)

    logger.info(payload, extra={'topic': prefix + str(sender_id), 'type': msg_type})

    f_read = open(logger.handlers[0].baseFilename, "r")
    last_line = f_read.readlines()[-1]
    elasticsearch.save_data(last_line)


def critical(msg, sender_id):

    logger = logging.getLogger()
    prefix = "" if "DCOP/" in str(sender_id) else "DCOP/"
    payload = json.dumps(msg)

    logger.critical(payload, extra={'topic': prefix + str(sender_id), 'type': 'CRITICAL'})

    f_read = open(logger.handlers[0].baseFilename, "r")
    last_line = f_read.readlines()[-1]
    elasticsearch.save_data(last_line)
