# coding: utf-8
import os
from setuptools import setup

from mockidp import __version__

def load_readme():
    with open('./README.md') as f:
        return str(f.read())


classifiers = [
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: 3.7"
]


config = {
    'name': 'mock-idp',
    'version': __version__,
    'description': 'Mock SAML 2.0 Identity Provider',
    'long_description': load_readme(),
    'long_description_content_type': 'text/markdown',
    'license': 'MIT',
    'author': 'Björn Skoglund',
    'author_email': 'bjorn.skoglund@icloud.com',
    'classifiers': classifiers,

    'install_requires': [
        'flask',
        'lxml',
        'PyYAML',
        'flask-script',
        'signxml',
        'nose'
    ],
    'packages': ['mockidp'],
    'include_package_data': True,
    'scripts': ['bin/mock-idp'],
}

setup(**config)
