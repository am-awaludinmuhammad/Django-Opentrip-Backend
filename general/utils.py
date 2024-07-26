import logging

def get_logger(name='django'):
    logger = logging.getLogger(name)
    return logger