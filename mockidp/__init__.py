# coding: utf-8
from flask import Flask

__version__ = "0.1.0"
app = Flask(__name__)

import mockidp.routes


def main(argv):
    app.run(debug=True)
