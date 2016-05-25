#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import logging
from logging import handlers

def init_log(logger_name, log_file):
    """Initialise the server logger and return it."""
    logger = logging.getLogger(logger_name)
    if len(logging.handlers):
        del(logger.handlers)
    log_format = logging.Formatter("[%(asctime)s] %(levelname)s :: %(message)s")
    log_file = "/var/log/" + log_file
    handler_server = logging.FileHandler(log_file, mode="a", encoding="utf-8") # Only work for linux system
    handler_server.setFormatter(log_format)
    handler_server.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)
    if not len(logging.handlers):
        logger.addHandler(handler_server)

    return logger
