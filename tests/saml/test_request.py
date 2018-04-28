# coding: utf-8
import base64

from nose.tools import eq_

from mockidp.saml.request import parse_request

INPUT = """<samlp:AuthnRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
    Version="2.0"
    ID="_2d099eab-b6bb-41fc-971a-389dec6a7ee5"
    Destination="http://localhost:5000/saml_login"
    IssueInstant="2017-06-07T11:06:02Z"
    ProtocolBinding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" >
    <saml:Issuer xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">http://mock-sp</saml:Issuer>
    <samlp:NameIDPolicy AllowCreate="true" Format="urn:mace:dir:attribute-def:displayName"/>
</samlp:AuthnRequest>
""".encode('utf-8')

encoded_input = base64.b64encode(INPUT)


def test_parse_request():
    req = parse_request(encoded_input)
    eq_('_2d099eab-b6bb-41fc-971a-389dec6a7ee5', req.id)
    eq_('http://mock-sp', req.sp_entity_id)
