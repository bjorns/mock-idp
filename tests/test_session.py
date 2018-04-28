# coding: utf-8
from nose.tools import eq_, ok_

from mockidp.saml.request import SAMLRequest

from mockidp.core.session import get_session


def test_get_session():
    user1 = dict(
        username='charlie'
    )
    request1 = SAMLRequest('abcd1234')

    user2 = dict(
        username='penelope'
    )
    request2 = SAMLRequest('abcd1235')

    session1 = get_session(user1, request1)

    ok_(len(session1.id) > 0)

    session2 = get_session(user1, request2)
    ok_(len(session2.id) > 0)
    eq_(session1.id, session2.id)

    session3 = get_session(user2, request2)
    ok_(len(session3.id) > 0)
    ok_(session3.id != session1.id)
