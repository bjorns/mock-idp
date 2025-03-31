import os
from flask import Flask, request, redirect, session, render_template_string, Response
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from jinja2 import Environment, FileSystemLoader

from saml import init_saml

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change for production

SAML_PATH = os.path.join(os.path.dirname(__file__), 'saml')

# HTML Templates
LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>Login</title>
</head>
<body>
    <h2>Welcome to the Onelogin SAML 2.0 Service Provider</h2>
    <form action="/login" method="POST">
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""

LOGGED_IN_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Welcome</title></head>
<body>
    <h2>Congratulations {{ name }}, you have been logged in!</h2>
</body>
</html>
"""

def init_saml_auth(req):
    return OneLogin_Saml2_Auth(req, custom_base_path=SAML_PATH)

def prepare_flask_request():
    """Prepares the Flask request for SAML."""
    url_data = request.host_url.rstrip('/')
    return {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'server_port': request.environ.get('SERVER_PORT', '8080'),
        'script_name': request.path,
        'get_data': request.args.copy(),
        'post_data': request.form.copy(),
    }

@app.route('/')
def index():
    if 'samlUserdata' in session:
        name = session['samlUserdata'].get('name', ['User'])[0]
        return render_template_string(LOGGED_IN_PAGE, name=name)
    return LOGIN_PAGE

@app.route('/login', methods=['POST'])
def login():
    """Initiates the SAML login process."""
    req = prepare_flask_request()
    auth = init_saml_auth(req)
    return redirect(auth.login())

@app.route('/metadata', methods=['GET'])
def metadata():
    req = prepare_flask_request()
    auth = init_saml_auth(req)
    saml_settings = auth.get_settings()
    body = saml_settings.get_sp_metadata()
    print(body)
    errors = saml_settings.validate_metadata(body)
    if len(errors) == 0:
        return Response(body, status=200, mimetype='application/xml')
    else:
        print("Error found on Metadata: %s" % (', '.join(errors)))
        return "", 500

@app.route('/acs', methods=['POST'])
def acs():
    """
    Assertion Consumer Service (ACS) - Handles the SAML assertion response from the IdP.
    """
    req = prepare_flask_request()
    auth = init_saml_auth(req)
    auth.process_response()

    errors = auth.get_errors()
    if errors:
        return f"Error: {errors}", 500

    if not auth.is_authenticated():
        return "Authentication failed", 401

    session['samlUserdata'] = auth.get_attributes()
    return redirect('/')

@app.route('/logout')
def logout():
    """Clears the session."""
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    init_saml()
    app.run(port=8080, debug=True)