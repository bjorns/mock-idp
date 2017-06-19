# coding: utf-8
from optparse import OptionParser

from mockidp import app
from mockidp.routes import conf


def main(argv):
    parser = OptionParser()
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Launch app in auto-reloading debug mode")

    options, args = parser.parse_args(args=argv)

    for sp in conf['service_providers']:
        print(f"Known Service Provider {sp['name']}")

    for username, data in conf['users'].items():
        print(f"Loaded user {username}")

    app.run(debug=options.debug, port=conf.get('port', 5000))
