# coding: utf-8
import logging
import sys
from optparse import OptionParser

from mockidp import app
from mockidp import core, saml

logging.basicConfig(level=logging.INFO, force=True)


def main(argv):
    logging.info("Running option parser")
    parser = OptionParser()
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Launch app in auto-reloading debug mode")
    parser.add_option("-p", "--port",
                      dest="port", default=5000,
                      help="Listen on port")
    parser.add_option("-H", "--host",
                      dest="host", default='127.0.0.1',
                      help="Listen on hostname")

    options, args = parser.parse_args(args=argv)

    conf, sessions = core.init()
    saml.init(conf)

    for sp in conf['service_providers']:
        logging.info("Known Service Provider %s", sp.get('name'))

    for username, data in conf['users'].items():
        logging.info("Loaded user %s", username)
    
    logging.info("Listening on %s:%s", options.host, options.port)
    app.run(debug=options.debug, host=options.host, port=options.port)
