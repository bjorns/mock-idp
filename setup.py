# coding: utf-8
from setuptools import setup

from mockidp import __version__

LONG_DESC = """SAML 2.0 Mock Identity Provider
===============================

Authentication testing environment for SAML2.0 service providers.

Ever needed to test an SSO setup but don't have access to the IDP for whatever
reason?

Mock IDP provides a SAML2.0 IDP using POST bindings without need for a user
database or complicated enterprise software setup.

"""

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
