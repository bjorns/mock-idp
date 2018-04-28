# coding: utf-8
from nose.tools import eq_, ok_

from mockidp.core.config import parse_config, get_service_provider


def test_parse_config():
    config = parse_config('tests/test_data/mock_config.yaml')
    sps = config['service_providers']
    eq_(1, len(sps))
    sp = sps[0]
    eq_('service_provider', sp['name'])
    eq_('http://localhost:4502', sp['url'])


def test_get_service_provider():
    config = {
        'service_providers': [
            {'name': "sp1"},
            {'name': "sp2"},
            {'name': "sp3"},
        ]
    }
    sp2 = get_service_provider(config, "sp2")
    ok_(sp2 is not None)
