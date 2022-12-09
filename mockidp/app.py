"""
Moving this out of __init__ in order to make e.g. setup.py not require dependencies.
"""
from flask import Flask

app = Flask(__name__)

import mockidp.saml.routes
import mockidp.routes
