import logging


def init_logging(loglevel: str):
    FORMAT = '%(asctime)-15s %(filename)s %(lineno)d %(levelname)s: %(message)s'
    logging.basicConfig(format=FORMAT, level=loglevel)
