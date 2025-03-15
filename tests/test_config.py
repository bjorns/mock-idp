from mockidp.core.config import parse_config, get_service_provider


def test_parse_config():
    config = parse_config('tests/test_data/mock_config.yaml')
    sps = config['service_providers']
    assert len(sps) == 1
    sp = sps[0]
    assert 'service_provider' == sp['name']
    assert 'http://localhost:4502' == sp['url']


def test_get_service_provider():
    config = {
        'service_providers': [
            {'name': "sp1"},
            {'name': "sp2"},
            {'name': "sp3"},
        ]
    }
    sp2 = get_service_provider(config, "sp2")
    assert sp2 is not None
