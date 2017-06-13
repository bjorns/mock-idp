# coding: utf-8
import base64
import time

import requests
from jinja2 import Environment, PackageLoader, select_autoescape
from lxml import etree
from signxml import XMLSigner

from mockidp.config import get_service_provider

env = Environment(
    loader=PackageLoader('mockidp', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
)


def saml_timestamp(epoch):
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(epoch))


env.filters['timestamp'] = saml_timestamp


def read_bytes(path):
    return open(path, 'rb').read()


def sign_assertions(response_str):
    """ Return signed response string """
    response_element = etree.fromstring(response_str)
    cert = read_bytes("keys/certificate.pem")
    key = read_bytes("keys/privkey.pem")
    for e in response_element.findall('{urn:oasis:names:tc:SAML:2.0:assertion}Assertion'):
        signer = XMLSigner(c14n_algorithm="http://www.w3.org/2001/10/xml-exc-c14n#",
                           signature_algorithm='rsa-sha1', digest_algorithm='sha1')
        signed_e = signer.sign(e, key=key, cert=cert)
        response_element.replace(e, signed_e)

    #response_element = XMLSigner().sign(response_element, key=key, cert=cert)
    return etree.tostring(response_element, pretty_print=True)


def post_session(config, session):
    _rendered_response = render_response(session, session.user)

    response = sign_assertions(_rendered_response)

    print("========= Response =======\n{}".format(response.decode('utf-8')))
    encoded_response = base64.b64encode(response)
    form_data = dict(
        SAMLResponse=encoded_response
    )

    service_provider = get_service_provider(config, session.sp_entity_id)
    url = service_provider['response_url']

    print(f"=== POSTing {form_data} to {url}")

    response = requests.post(url, auth=("admin", 'admin'), data=form_data)
    if response.status_code != 200:
        raise Exception(f"Failed to post data to Service Provider: {response}")


def render_response(session, user):
    template = env.get_template('saml_response.xml')
    params = dict(
        session=session,
        user=user
    )
    response = template.render(params)

    return response
