# coding: utf-8

from base64 import b64decode
from io import BytesIO

from lxml import etree


class SAMLRequest:
    def __init__(self, _id, sp_entity_id=None):
        self.id = _id
        self.sp_entity_id = sp_entity_id


def parse_request(request_body):
    """ Expectes the source base64 encoded SAMLRequest header """
    request_xml = b64decode(request_body).decode('utf-8')

    srcbuf = BytesIO(request_xml.encode('utf-8'))
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
    sp_entity_id = root_node.find('{urn:oasis:names:tc:SAML:2.0:assertion}Issuer').text
    saml_request = SAMLRequest(_id, sp_entity_id)
    return saml_request
