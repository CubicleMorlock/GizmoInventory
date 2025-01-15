import logging
import logging.handlers

def make_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    log_format = '%(levelname)s [%(asctime)s %(module)s:%(funcName)s (line %(lineno)d, thread %(threadName)s)] - %(message)s'
    formatter = logging.Formatter(log_format)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
