# coding: utf-8
import logging

from . import config
from . import auth
from . import session


def init():
    config_filename = config.locate_config_file()
    logging.info("Loading config %s", config_filename)
    conf = config.parse_config(config_filename)

    return conf, None
