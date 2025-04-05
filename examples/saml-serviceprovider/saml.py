"""
Instead of requiring the user to configure the certificate for the service
provider before using it, we just generate certificates as part of booting. This consists of

* Generating a private key
* Generating a certificate signing request
* Generating a self-signing the certificate
* Generating a SAML settings.json with the certificate included.
"""
from base64 import b64encode
from os.path import join as joinpath, dirname

from jinja2 import Environment, FileSystemLoader

from mockidp.core.certs import generate_private_key, generate_certificate_signing_request, generate_certificate
from template import load_str


TEMPLATES_PATH = joinpath(dirname(__file__), 'templates')

def init_saml():
    private_key_path = generate_private_key("saml-sp/private-key.pem")
    signing_request_path = generate_certificate_signing_request(private_key_path, "saml-sp/service-provider.csr")
    certificate_path = generate_certificate(private_key_path, signing_request_path, "saml-sp/service-provider.crt")
    render_settings_json(load_str(certificate_path))


def render_settings_json(certificate: str):
    loader = FileSystemLoader(searchpath=TEMPLATES_PATH)
    env = Environment(loader=loader)
    env.filters['b64encode'] = lambda s: b64encode(s.encode('utf-8')).decode('utf-8')
    template = env.get_template('settings.json')
    with open(joinpath(dirname(__file__), 'saml/settings.json'), 'w') as f:
        f.write(template.render(servide_provider_cert=certificate))

