#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import logging
from logging import handlers

def init_log(logger_name, log_file):
    """Initialise the server logger if he doesn't exist and return it."""
    log_format = logging.Formatter("[%(asctime)s] %(levelname)s :: %(message)s")

    handler = logging.FileHandler(log_file, mode="a", encoding="utf-8") # Only work for linux system

    handler.setFormatter(log_format)
    handler.setLevel(logging.INFO)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    for bis_handler in logger.handlers:
        print bis_handler
