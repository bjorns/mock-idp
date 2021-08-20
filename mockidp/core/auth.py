# coding: utf-8
import logging

LOGIN_SUCCESS = 0
LOGIN_FAIL = 1


def login_user(config, username, password):
    """ Authenticate user """

    user = config['users'].get(username)
    if user is None:
        logging.error(" Requested user '%s' does not exist. Options are %s", username, list(config['users'].keys()))
        return LOGIN_FAIL, None

    user['username'] = username
    if user['password'] == password:
        logging.info("Successfully logged in %s", username)
        return LOGIN_SUCCESS, user
    return LOGIN_FAIL, None

def logout_user(config, username):
    """ Logout user """
    user = config['users'].get(username)
    user['username'] = username
    return LOGIN_SUCCESS, None
