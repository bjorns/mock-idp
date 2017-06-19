# coding: utf-8
from flask import Flask

__version__ = "0.1.0"
app = Flask(__name__)

import mockidp.routes
from mockidp.routes import conf


def main(argv):
    for sp in conf['service_providers']:
        print(f"Known Service Provider {sp['name']}")

    for username, data in conf['users'].items():
        print(f"Loaded user {username}")

    app.run(debug=False, port=conf.get('port', 5000))
