# coding: utf-8
import sys
from optparse import OptionParser

from mockidp import app
from mockidp.routes import conf


def main(argv):
    print("Running option parser")
    parser = OptionParser()
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Launch app in auto-reloading debug mode")

    options, args = parser.parse_args(args=argv)

    for sp in conf['service_providers']:
        print(f"Known Service Provider {sp['name']}")

    for username, data in conf['users'].items():
        print(f"Loaded user {username}")

    sys.stdout.flush()
    app.run(debug=options.debug, host="0.0.0.0", port=conf.get('port', 5000))
