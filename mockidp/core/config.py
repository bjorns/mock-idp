# coding: utf-8
import logging
import yaml
import os
import pkg_resources

LOCAL_CONFIG = "{}/mockidp.yaml".format(os.path.curdir)
HOME_DIR_CONFIG = "{}/.mockidp.yaml".format(os.path.expanduser("~"))
GLOBAL_CONFIG = "/etc/mockidp.yaml"


def locate_config_file():
    """ Return a path to a config to use accoding to standard preference rules """

    logging.info("Checking if %s is a file", LOCAL_CONFIG)
    if os.path.isfile(LOCAL_CONFIG):
        return LOCAL_CONFIG
    if os.path.isfile(HOME_DIR_CONFIG):
        return HOME_DIR_CONFIG
    if os.path.isfile(GLOBAL_CONFIG):
        return GLOBAL_CONFIG
    resource = pkg_resources.resource_filename('mockidp', 'resources/default_config.yaml')
    return resource


def parse_config(filename):
    with open(filename) as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
        return config


def get_service_provider(config, name):
    service_providers = config['service_providers']
    if type(service_providers) != list:
        raise Exception(f"Unexpected obj {service_providers}")
    matches = list(filter(lambda x: x['name'] == name, service_providers))
    if len(matches) != 1:
        raise Exception(f"Unable to locate service provider {name}, available {service_providers}")
    return matches[0]
