import time

from mockidp.saml.response import saml_timestamp


def test_saml_timestamp():
    t = time.time()

    x = saml_timestamp(t)

    assert len(x) > 1
