import base64
import os.path

from jinja2 import Environment, FileSystemLoader

TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), 'templates')



def init_ssl():
    loader = FileSystemLoader(searchpath=TEMPLATES_PATH)
    env = Environment(loader=loader)
    env.filters['b64encode'] = lambda s: base64.b64encode(s.encode('utf-8')).decode('utf-8')
    template = env.get_template('settings.json')
    # TODO: Generate SSL certs

    # Render to file
    with open(os.path.join(os.path.dirname(__file__), 'saml/settings.json'), 'w') as f:
        f.write(template.render(servide_provider_cert='foobar'))
