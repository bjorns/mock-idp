# coding: utf-8
import time

from nose.tools import ok_

from mockidp.saml.response import saml_timestamp


def test_saml_timestamp():
    t = time.time()

    x = saml_timestamp(t)

    ok_(len(x) > 1)
