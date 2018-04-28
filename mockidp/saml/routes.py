import flask
from mockidp import app

from mockidp.auth import login_user, LOGIN_SUCCESS
from mockidp.config import parse_config, locate_config_file
from mockidp.session import get_session

from .request import parse_request
from .response import create_auth_response

open_saml_requests = dict()

config_filename = locate_config_file()
print(f"Loading config {config_filename}")
conf = parse_config(config_filename)


@app.route('/saml', methods=['POST'])
def begin_login():
    saml_request = flask.request.form['SAMLRequest']
    req = parse_request(saml_request)

    print(f"Storing request {req.id}")
    open_saml_requests[req.id] = req

    response = flask.make_response(flask.redirect("/saml/login", code=302))
    response.set_cookie('mockidp_request_id', value=req.id)
    return response


@app.route('/saml', methods=['GET'])
def begin_login_get():
    saml_request = flask.request.args['SAMLRequest']
    print(f"Got saml_request {saml_request}")

    req = parse_request(saml_request)

    print(f"Storing request {req.id}")
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
