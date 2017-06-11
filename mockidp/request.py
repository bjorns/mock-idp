# coding: utf-8

from base64 import b64decode
from io import BytesIO

from lxml import etree


class SAMLRequest:
    def __init__(self, _id):
        self.id = _id


def parse_request(saml_request):
    """ Expectes the source base64 encoded SAMLRequest header """
    decoded_request = b64decode(saml_request).decode('utf-8')

    srcbuf = BytesIO(decoded_request.encode('utf-8'))
    doc = etree.parse(srcbuf)

    pretty_xml = etree.tostring(doc.getroot(), pretty_print=True).decode('utf-8')
    print("=== Request ====\n{}\n=========".format(str(pretty_xml)))

    req = _parse_request_xml(doc)
    return req


def _parse_request_xml(doc):
    """ Expects xml.etree.ElementTree """
    root_node = doc.getroot()
    print("=== xml: {}".format(root_node))
    _id = root_node.get('ID')
    saml_request = SAMLRequest(_id)
    return saml_request
