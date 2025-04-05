"""
This package implements the SAML2.0 POST authentication flow.
"""
import logging

from mockidp.core.certs import generate_private_key, generate_certificate_signing_request, generate_certificate

from . import routes

def init_certs():
    """
    Generate the main IDP certificate and corrsponding private key.
    """
    private_key_path = generate_private_key("idp/private-key.pem")
    signing_request_path = generate_certificate_signing_request(private_key_path, "idp/signing_request.csr")
    certificate_path = generate_certificate(private_key_path, signing_request_path, "idp/certificate.crt")
    return certificate_path

def init(conf):
    """ Initialize HTTP routes. """
    certificate_path = init_certs()
    logging.info("Using certificate %s", certificate_path)
    routes.init(conf)
