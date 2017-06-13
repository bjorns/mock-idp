#!/usr/bin/env python3
import flask
from mockidp import app

from mockidp.auth import login_user, LOGIN_SUCCESS
from mockidp.config import parse_config
from mockidp.request import parse_request
from mockidp.response import create_auth_response
from mockidp.session import get_session

conf = parse_config('config.yaml')
open_saml_requests = dict()


@app.route('/saml_login', methods=['POST'])
def begin_login():
    saml_request = flask.request.form['SAMLRequest']
    req = parse_request(saml_request)

    print(f"Storing request {req.id}")
    open_saml_requests[req.id] = req

    response = flask.make_response(flask.redirect("/login", code=302))
    response.set_cookie('mockidp_request_id', value=req.id)
    return response


@app.route('/login', methods=['GET'])
def login_view():
    return flask.render_template('login.html')


@app.route('/auth', methods=['POST'])
def authenticate():
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')

    status, user = login_user(conf, username, password)
    if status == LOGIN_SUCCESS:
        saml_req_id = flask.request.cookies.get('mockidp_request_id')
        if saml_req_id not in open_saml_requests:
            return '404: Missing login session', 404
        saml_request = open_saml_requests[saml_req_id]
        session = get_session(user, saml_request)
        url, saml_response = create_auth_response(conf, session)
        return flask.render_template('auth_response.html', post_url=url, saml_response=saml_response)
    else:
        flask.flash(f"Incorrect username or password {username}")
        return flask.redirect("/login", code=302)


@app.route('/css/<path:path>')
def send_js(path):
    return flask.send_from_directory('resources/css', path)
