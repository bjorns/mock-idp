# coding: utf-8
from flask import Flask

__version__ = "0.2.1"
app = Flask(__name__)

import mockidp.saml.routes
import mockidp.routes
