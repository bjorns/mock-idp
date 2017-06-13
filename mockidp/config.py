# coding: utf-8
import yaml


def parse_config(filename):
    f = open(filename)
    config = yaml.load(f)
    return config


def get_service_provider(config, name):
    service_providers = config['service_providers']
    if type(service_providers) != list:
        raise Exception(f"Unexpected obj {service_providers}")
    matches = list(filter(lambda x: x['name'] == name, service_providers))
    if len(matches) != 1:
        raise Exception(f"Unable to locate service provider {name}, available {service_providers}")
    return matches[0]
