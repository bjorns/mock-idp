# coding: utf-8
import sys
from optparse import OptionParser

from mockidp import app
from mockidp import core, saml


def main(argv):
    print("Running option parser")
    parser = OptionParser()
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Launch app in auto-reloading debug mode")
    parser.add_option("-p", "--port",
                      dest="port", default=5000,
                      help="Listen on port")

    options, args = parser.parse_args(args=argv)

    conf, sessions = core.init()
    saml.init(conf)

    for sp in conf['service_providers']:
        print(f"Known Service Provider {sp['name']}")

    for username, data in conf['users'].items():
        print(f"Loaded user {username}")

    sys.stdout.flush()
    app.run(debug=options.debug, host="0.0.0.0", port=options.port)
