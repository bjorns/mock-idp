#!/usr/bin/env python3
import sys

from lxml import etree
from signxml import XMLVerifier


def read_bytes(path):
    return open(path, 'r').read()


def sign_assertions(response_str):
    """ Return signed response string """
    response_element = etree.fromstring(response_str)
    cert = read_bytes("keys/cert.pem")
    for e in response_element.findall('{urn:oasis:names:tc:SAML:2.0:assertion}Assertion'):
        verifier = XMLVerifier()
        data = verifier.verify(e, x509_cert=cert).signed_xml


def main(filename):
    input_data = open(filename, 'r').read()
    sign_assertions(input_data)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write("usage: ./saml-sign.py <input_file>\n")
        sys.exit(-1)

    main(sys.argv[1])
