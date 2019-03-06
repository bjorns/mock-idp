# coding: utf-8
LOGIN_SUCCESS = 0
LOGIN_FAIL = 1


def login_user(config, username, password):
    """ Authenticate user """

    user = config['users'].get(username)
    if user is None:
        print(f"error: Requested user '{username}' does not exist. Options are {list(config['users'].keys())}")
        return LOGIN_FAIL, None

    user['username'] = username
    if user['password'] == password:
        print(f"Successfully logged in {username}")
        return LOGIN_SUCCESS, user
    return LOGIN_FAIL, None

def logout_user(config, username):
    """ Logout user """
    user = config['users'].get(username)
    user['username'] = username
    return LOGIN_SUCCESS, None
