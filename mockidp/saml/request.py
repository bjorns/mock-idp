# coding: utf-8
import logging
import zlib
from base64 import b64decode
from io import BytesIO

from lxml import etree


class SAMLRequest:
    def __init__(self, _id, sp_entity_id=None, name_id=None):
        self.id = _id
        self.sp_entity_id = sp_entity_id
        self.name_id = name_id

def try_deflate(request_body):
    try:
        return zlib.decompress(request_body, -15)
    except Exception as e:
        logging.exception("Failed to defalate")        
        return request_body


def parse_request(request_body):
    """ Expectes the source base64 encoded SAMLRequest header """
    request_xml = b64decode(request_body)
    request_xml = try_deflate(request_xml)
    srcbuf = BytesIO(request_xml)

    doc = etree.parse(srcbuf)

    req = _parse_request_xml(doc)
    return req


def _parse_request_xml(doc):
    """ Expects xml.etree.ElementTree """
    root_node = doc.getroot()
    _id = root_node.get('ID')
    sp_entity_id = root_node.find('{urn:oasis:names:tc:SAML:2.0:assertion}Issuer').text
    name_id_node = root_node.find('{urn:oasis:names:tc:SAML:2.0:assertion}NameID')
    
    name_id = getattr(name_id_node, 'text', '')
    saml_request = SAMLRequest(_id, sp_entity_id, name_id)
    return saml_request
