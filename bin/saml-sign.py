#!/usr/bin/env python3
import sys

from lxml import etree
from signxml import XMLSigner


def read_bytes(path):
    return open(path, 'rb').read()


def sign_assertions(response_str):
    """ Return signed response string """
    response_element = etree.fromstring(response_str)
    cert = read_bytes("keys/cert.pem")
    key = read_bytes("keys/key.pem")
    for e in response_element.findall('{urn:oasis:names:tc:SAML:2.0:assertion}Assertion'):
        signer = XMLSigner(c14n_algorithm="http://www.w3.org/2001/10/xml-exc-c14n#",
                           signature_algorithm='rsa-sha1', digest_algorithm='sha1')
        signed_e = signer.sign(e, key=key, cert=cert)
        response_element.replace(e, signed_e)

    return etree.tostring(response_element, pretty_print=True)


def main(filename):
    input_data = open(filename, 'r').read()
    output = sign_assertions(input_data)
    print(output.decode('utf-8'))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write("usage: ./saml-sign.py <input_file>\n")
        sys.exit(-1)

    main(sys.argv[1])
