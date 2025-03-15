from mockidp.core.auth import login_user, LOGIN_SUCCESS, LOGIN_FAIL

config = {'users': {
    'charlie': {
        'password': 'secret',
        'name': 'charlie brown'
    }
}
}

assert LOGIN_SUCCESS != LOGIN_FAIL


def test_successful_login():
    status, user = login_user(config, 'charlie', 'secret')
    assert LOGIN_SUCCESS == status
    assert 'charlie brown' == user['name']


def test_incorrect_password():
    status, user = login_user(config, 'charlie', 'wrongpassword')
    assert LOGIN_FAIL == status
    assert user is None


def test_non_existing_user():
    status, user = login_user(config, 'penelope', 'anypassword')
    assert LOGIN_FAIL == status
    assert user is None
