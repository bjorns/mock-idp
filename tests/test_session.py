# coding: utf-8
from nose.tools import eq_, ok_

from mockidp.session import get_session


def test_get_session():
    user1 = dict(
        username='charlie'
    )
    request_id1 = 'abcd1234'

    user2 = dict(
        username='penelope'
    )
    request_id2 = 'abcd1235'

    session1 = get_session(user1, request_id1)

    ok_(len(session1.id) > 0)

    session2 = get_session(user1, request_id2)
    ok_(len(session2.id) > 0)
    eq_(session1.id, session2.id)

    session3 = get_session(user2, request_id2)
    ok_(len(session3.id) > 0)
    ok_(session3.id != session1.id)
