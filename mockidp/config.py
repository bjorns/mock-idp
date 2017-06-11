# coding: utf-8
import yaml


def parse_config(filename):
    f = open(filename)
    config = yaml.load(f)
    return config
