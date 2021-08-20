import logging
import flask
from mockidp import app

from mockidp.core.auth import login_user, logout_user, LOGIN_SUCCESS
from mockidp.core.session import get_session, retrieve_session

from .request import parse_request
from .response import create_auth_response, create_logout_response

open_saml_requests = dict()
conf = None


def init(_conf):
    global conf
    conf = _conf


@app.route('/saml', methods=['POST'])
def begin_login():
    saml_request = flask.request.form['SAMLRequest']
    req = parse_request(saml_request)

    logging.info("Storing request %s", req.id)
    open_saml_requests[req.id] = req

    response = flask.make_response(flask.redirect("/saml/login", code=302))
    response.set_cookie('mockidp_request_id', value=req.id)
    return response


@app.route('/saml', methods=['GET'])
def begin_login_get():
    saml_request = flask.request.args['SAMLRequest']
    logging.info("Got saml_request %s", saml_request)

    req = parse_request(saml_request)

    logging.info("Storing request %s", req.id)
    open_saml_requests[req.id] = req

    response = flask.make_response(flask.redirect("/saml/login", code=302))
    response.set_cookie('mockidp_request_id', value=req.id)
    return response


@app.route('/saml/login', methods=['GET'])
def login_view():
    return flask.render_template('login.html')


@app.route('/saml/auth', methods=['POST'])
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
        return flask.redirect("/saml/login", code=302)


@app.route('/saml/logout', methods=['GET'])
def logout_view():
    """ <?xml version="1.0"?>
        <samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol" 
                xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion" ID="_de4a72a1d3fd94ba287289b5b81987884320a6d5eb"
                Version="2.0" 
                IssueInstant="2019-03-06T18:32:52.137Z" 
                Destination="http://mockidp:5000/saml/logout">
            <saml:Issuer>local:onehope:web</saml:Issuer>
            <saml:NameID Format="urn:oasis:names:tc:SAML:2.0:nameid-format:persistent">charlie</saml:NameID>
            <samlp:SessionIndex>
                _be9967abd904ddcae3c0eb4189adbe3f71e327cf93
            </samlp:SessionIndex>
        </samlp:LogoutRequest> """
    saml_request = flask.request.args['SAMLRequest']
    req = parse_request(saml_request)
    username = req.name_id
    logging.info("Logging out %s", username)
    session = retrieve_session(username)
    logging.info("Session is %s", session)
    url, saml_response = create_logout_response(conf, session)
    return flask.render_template('saml/logout.html', post_url=url, saml_response=saml_response)
