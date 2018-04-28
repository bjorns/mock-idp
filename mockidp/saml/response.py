# coding: utf-8
import base64
import time
import pkg_resources

from jinja2 import Environment, PackageLoader, select_autoescape
from lxml import etree
from signxml import XMLSigner

from mockidp.core.config import get_service_provider

env = Environment(
    loader=PackageLoader('mockidp', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
)


def saml_timestamp(epoch):
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(epoch))


env.filters['timestamp'] = saml_timestamp


def read_bytes(path):
    filename = pkg_resources.resource_filename('mockidp', path)
    return open(filename, 'rb').read()


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


def create_auth_response(config, session):
    rendered_response = render_response(session, session.user)

    signed_response = sign_assertions(rendered_response)

    encoded_response = base64.b64encode(signed_response).decode('utf-8')

    service_provider = get_service_provider(config, session.sp_entity_id)
    url = service_provider['response_url']

    return url, encoded_response


def render_response(session, user):
    template = env.get_template('saml_response.xml')
    params = dict(
        session=session,
        user=user
    )
    response = template.render(params)

    return response
