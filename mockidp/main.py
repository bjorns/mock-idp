# coding: utf-8

from mockidp.routes import conf
from mockidp import app


def main(argv):

    for sp in conf['service_providers']:
        print(f"Known Service Provider {sp['name']}")

    for username, data in conf['users'].items():
        print(f"Loaded user {username}")

    app.run(debug=True, port=conf.get('port', 5000))
