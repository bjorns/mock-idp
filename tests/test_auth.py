# coding: utf-8
from nose.tools import eq_, ok_

from mockidp.core.auth import login_user, LOGIN_SUCCESS, LOGIN_FAIL

config = {'users': {
    'charlie': {
        'password': 'secret',
        'name': 'charlie brown'
    }
}
}

ok_(LOGIN_SUCCESS != LOGIN_FAIL)


def test_successful_login():
    status, user = login_user(config, 'charlie', 'secret')
    eq_(LOGIN_SUCCESS, status)
    eq_('charlie brown', user['name'])


def test_incorrect_password():
    status, user = login_user(config, 'charlie', 'wrongpassword')
    eq_(LOGIN_FAIL, status)
    eq_(None, user)


def test_non_existing_user():
    status, user = login_user(config, 'penelope', 'anypassword')
    eq_(LOGIN_FAIL, status)
    eq_(None, user)
