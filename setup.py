# coding: utf-8
from setuptools import setup

from mockidp import __version__

LONG_DESC = """SAML 2.0 Mock Identity Provider
===============================

Authentication testing environment for SAML2.0 service providers.
"""

classifiers = [
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 4 - Beta',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development',

    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    "Programming Language :: Python :: 3.6"
]


config = {
    'name': 'mock-idp',
    'version': __version__,
    'description': 'Mock SAML 2.0 Identity Provider',
    'long_description': LONG_DESC,
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
