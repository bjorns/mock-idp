"""
This package implements the SAML2.0 POST authentication flow.
"""
from . import routes


def init(conf):
    """ Initialize HTTP routes. """
    routes.init(conf)
