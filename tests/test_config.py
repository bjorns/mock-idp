# coding: utf-8
from nose.tools import eq_

from mockidp.config import parse_config


def test_parse_config():
    config = parse_config('tests/test_data/mock_config.yaml')
    sps = config['service_providers']
    eq_(1, len(sps))
    sp = sps[0]
    eq_('service_provider', sp['name'])
    eq_('http://localhost:4502', sp['url'])
