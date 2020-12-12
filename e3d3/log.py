import os
import logging


FORMAT = logging.Formatter('%(asctime)s[%(levelname)s]: %(relpath)s, line %(lineno)d - %(message)s')


class RelpathFilter(logging.Filter):
    def filter(self, record):
        record.relpath = os.path.relpath(record.pathname)


def get(name):
    return logging.getLogger(name)


file_handler = logging.FileHandler('e3d3.log', 'w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(FORMAT)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(FORMAT)

logger = logging.getLogger(__name__)
logger.addFilter(RelpathFilter())
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.info('Start E3D3')
logger.info('Start log subsystem.')