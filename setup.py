import os
from setuptools import setup, find_packages

from mockidp.__version__ import version


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
    'version': version,
    'description': 'Mock SAML 2.0 Identity Provider',
    'long_description': load_readme(),
    'long_description_content_type': 'text/markdown',
    'license': 'MIT',
    'author': 'Björn Skoglund',
    'author_email': 'bjorn.skoglund@icloud.com',
    'classifiers': classifiers,
    'install_requires': [
        'flask==3.1.0',
        'lxml==5.3.1',
        'PyYAML==6.0.2',
        'flask-script==2.0.6',
        'signxml==4.0.3',
    ],
    'extras_require': {
        'dev': [
            'pytest==8.3.5',
            'twine==6.1.0',
            'setuptools==76.0.0'
        ]
    },
    'packages': find_packages(),
    'package_data': {'mockidp': [
        'resources/*',
        'resources/css/*',
        'resources/img/*',
        'keys/*',
        'templates/*',
        'templates/saml/*',
    ]},
    'include_package_data': True,
    'scripts': ['bin/mock-idp'],
}

setup(**config)
