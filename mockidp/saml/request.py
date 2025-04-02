from zlib import decompress
from base64 import b64decode
from io import BytesIO

from lxml import etree


class SAMLRequest:
    """
    Data object for a SAML request.
    """
    def __init__(self, _id, sp_entity_id=None, name_id=None, idp_id=None, assertion_consumer_service_url=None):
        self.id = _id
        self.sp_entity_id = sp_entity_id
        self.name_id = name_id
        self.idp_id = idp_id
        self.assertion_consumer_service_url = assertion_consumer_service_url

def try_deflate(request_body):
    return decompress(request_body, -15)


def parse_request(request_body):
    """ Expectes the source base64 encoded SAMLRequest header """
    request_xml = b64decode(request_body)
    request_xml = try_deflate(request_xml)
    print(f"=== " + request_xml.decode('utf-8'))
    srcbuf = BytesIO(request_xml)

    doc = etree.parse(srcbuf)

    req = _parse_request_xml(doc)
    return req


def _parse_request_xml(doc):
    """ Expects xml.etree.ElementTree """
    root_node = doc.getroot()
    _id = root_node.get('ID')
    assertion_consumer_service_url = root_node.get('AssertionConsumerServiceURL')
    sp_entity_id = root_node.find('{urn:oasis:names:tc:SAML:2.0:assertion}Issuer').text
    name_id_node = root_node.find('{urn:oasis:names:tc:SAML:2.0:assertion}NameID')
    
    name_id = getattr(name_id_node, 'text', '')
    saml_request = SAMLRequest(_id=_id, sp_entity_id=sp_entity_id, name_id=name_id,
                               assertion_consumer_service_url=assertion_consumer_service_url)
    return saml_request
