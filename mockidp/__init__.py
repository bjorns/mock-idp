# coding: utf-8
from flask import Flask

__version__ = "0.4.2"
app = Flask(__name__)

import mockidp.saml.routes
import mockidp.routes
