"""
Instead of requiring the user to configure the certificate for the service
provider before using it, we just generate certificates as part of booting. This consists of

* Generating a private key
* Generating a certificate signing request
* Generating a self-signing the certificate
* Generating a SAML settings.json with the certificate included.
"""
from base64 import b64encode
from subprocess import Popen, PIPE
from os.path import join as joinpath, dirname

from jinja2 import Environment, FileSystemLoader

TARGET_DIR = joinpath(dirname(__file__), 'saml')
TEMPLATES_PATH = joinpath(dirname(__file__), 'templates')


def init_saml():
    private_key_path = generate_private_key("private-key.pem")
    signing_request_path = generate_certificate_signing_request(private_key_path, "service-provider.csr")
    certificate_path = generate_certificate(private_key_path, signing_request_path, "service-provider.crt")
    render_settings_json(_load_str(certificate_path))

def generate_private_key(filename: str) -> str:
    result_file = joinpath(TARGET_DIR, filename)
    cmd = Popen(["openssl", "genrsa", "-out", result_file, "2048"],
                stdout=PIPE, stderr=PIPE)
    cmd.communicate()
    return result_file


def generate_certificate_signing_request(private_key_file: str, filename: str) -> str:
    result_file = joinpath(TARGET_DIR, filename)
    cmd = Popen(["openssl", "req", "-new", "-key", private_key_file, "-out", result_file, "-subj",
                 "/C=US/ST=New York/L=New York City/O=Some Org/OU=Some Department/CN=example.com/emailAddress=charlies@peanuts.com"],
                stdout=PIPE, stderr=PIPE)
    cmd.communicate()
    return result_file

def generate_certificate(private_key_file: str, signing_request_file: str, filename: str) -> str:
    result_file = joinpath(TARGET_DIR, filename)
    cmd = Popen(["openssl", "x509", "-req", "-days", "365", "-in", signing_request_file, "-signkey", private_key_file, "-out", result_file],
                stdout=PIPE, stderr=PIPE)
    cmd.communicate()
    return result_file


def render_settings_json(certificate: str):
    loader = FileSystemLoader(searchpath=TEMPLATES_PATH)
    env = Environment(loader=loader)
    env.filters['b64encode'] = lambda s: b64encode(s.encode('utf-8')).decode('utf-8')
    template = env.get_template('settings.json')
    with open(joinpath(dirname(__file__), 'saml/settings.json'), 'w') as f:
        f.write(template.render(servide_provider_cert=certificate))


def _load_str(filepath:str) -> str:
    with open(filepath, 'r') as f:
        return f.read()
