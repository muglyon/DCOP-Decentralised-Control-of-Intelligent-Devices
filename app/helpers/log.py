import logging
from pythonjsonlogger import jsonlogger

FORMAT_STR = "{'asctime': '%(asctime)s', 'topic': '%(topic)s', 'content': '%(message)s', 'level': '%(levelname)s'}"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"


def setup_custom_logger(file_name):
    logging.basicConfig(format=FORMAT_STR, filename=file_name, level=logging.INFO, datefmt=DATE_FORMAT)

    handler = logging.StreamHandler()
    handler.setFormatter(jsonlogger.JsonFormatter(FORMAT_STR))

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def info(msg, topic):
    logging.getLogger().info(msg, extra={'topic': topic})

