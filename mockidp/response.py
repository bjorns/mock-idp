# coding: utf-8
import time

import requests
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('mockidp', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
)


def saml_timestamp(epoch):
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(epoch))

env.filters['timestamp'] = saml_timestamp


def post_session(session):
    response = render_response(session, session.user)
    print("========= Response =======\n{}".format(response))


def render_response(session, user):
    template = env.get_template('saml_response.xml')
    params = dict(
        session=session,
        user=user
    )
    response = template.render(params)

    return response
