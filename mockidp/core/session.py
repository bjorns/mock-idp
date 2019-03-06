# coding: utf-8
import time

_sessions = dict()
_next_session_id = 0


class Session:
    def __init__(self, user, request):
        self.user = user
        self.request_id = request.id
        self.sp_entity_id = request.sp_entity_id
        self.id = _generate_session_id(user['username'])
        self.created = time.time()


def get_session(user, request):
    username = user['username']
    if has_session(username):
        return _sessions[username]
    else:
        session = Session(user, request)
        _sessions[username] = session
        return session

def retrieve_session(username):
    if has_session(username):
        return _sessions[username]
    else:
        raise Exception(f'Failed to locate session for {username}')

def has_session(username):
    return username in _sessions


def _generate_session_id(username):
    global _next_session_id
    _next_session_id += 1
    return f"{username}_{_next_session_id}"
