# coding: utf-8
from . import config
from . import auth
from . import session


def init():
    config_filename = config.locate_config_file()
    print(f"Loading config {config_filename}")
    conf = config.parse_config(config_filename)

    return conf, None
