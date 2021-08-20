#!/usr/bin/env python3
import logging
import flask
from mockidp import app

from mockidp.core.config import parse_config, locate_config_file

config_filename = locate_config_file()
logging.info("Loading config %s", config_filename)
conf = parse_config(config_filename)
open_saml_requests = dict()


@app.route('/css/<path:path>')
def send_js(path):
    return flask.send_from_directory('resources/css', path)


@app.route('/img/<path:path>')
def images(path):
    return flask.send_from_directory('resources/img', path)


@app.route('/debug')
def debug():
    return flask.render_template('auth_response_debug.html')
