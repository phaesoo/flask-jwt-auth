import logging


def init_logger(name):
    formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
    log_handler = handlers.TimedRotatingFileHandler(filename='./log/test.log', when='midnight', interval=1, encoding='utf-8')
    log_handler.setFormatter(formatter)
    log_handler.suffix = "%Y%m%d"

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(log_handler)
