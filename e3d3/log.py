import os
import logging


FORMAT = logging.Formatter('%(asctime)s[%(levelname)s]: %(relpath)s, line %(lineno)d - %(message)s')


class RelpathFilter(logging.Filter):
    def filter(self, record):
        record.relpath = os.path.relpath(record.pathname)
        return record


def get(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addFilter(RelpathFilter())
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


file_handler = logging.FileHandler('./e3d3.log', mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(FORMAT)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(FORMAT)

logger = logging.getLogger('E3D3')
logger.setLevel(logging.DEBUG)
logger.addFilter(RelpathFilter())
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.info('Start E3D3')
logger.info('Start log subsystem.')