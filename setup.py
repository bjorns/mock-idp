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


## Installation

Install and run mock-idp using Pip:

    $ pip3 install mock-idp
    $ mock-idp
    ...

## Configuration File

To override the system configuration create a config file. The service loads 
config files in the following order:

1. `mockidp.yaml` in the current working directory
2. `~/.mockidp.yaml` in your home directory
3. `/etc/mockidp.yaml` in the global config directory
4. internal default config file shipped with the service package

Here is a sample (copy of built-in config) file to start with:

```
service_providers:
  - name: "local:service:author"
    response_url: "http://localhost:3000/saml_login"

users:
  charlie:
    first_name: "Charlie"
    last_name: "Brown"
    email: "charlie@gmail.com"
    password: snoopy
  linus:
    first_name: "Linus"
    last_name: "van Pelt"
    email: "linus@gmail.com"
    password: pumpkin
  lucy:
    password: charlie
    first_name: "Lucy"
    last_name: "van Pelt"
    email: "lucy@gmail.com"
  peppermint:
    first_name: "Peppermint"
    last_name: "Patty"
    email: "peppermint@gmail.com"
    password: peppermint
```

### Service providers

For each service provider (client) that uses the identity provider, an entry in
the service providers section of the config is needed. It has two values:

    service_providers:
      - name: "local:aem:author"
        response_url: "http://localhost:14502/saml_login"


* **name** is the service provider entity id that the service provider sends
    with each request.
* **response_url** is the public url of the service provider. Once login has
    been completed, the browser will be redirected to this url.

### Users

Users is a fairly self explanatory list of user credentials recognized
by the IDP:

    users:
      charlie:
        first_name: "Charlie"
        last_name: "Brown"
        email: "charlie@gmail.com"
        password: snoopy
        roles:
          - administrators


## Configuring a generic Service Provider

* Mock-IDP supports the POST binding protocol of SAML2.0.
* By default mock-idp runs on port 5000 and the binding path is /saml.
* the response message provides four attributes:
    - uid: The username
    - email: the user email address
    - firstName: The users first name
    - lastName: The users last name
* The logout path is /saml/logout

### Certificate keys

To generate a service provider Certificate, run the following commands:

    $ openssl genrsa -out saml.pem 2048
    $ openssl req -new -key saml.pem -out saml.csr
    $ openssl x509 -req -days 365 -in saml.csr -signkey saml.pem -out saml.crt

This will produce three files:

* __saml.pem__ - The private key
* __saml.csr__ - The certificate signing request
* __saml.crt__ - The final certificate

Refer to your service provider documentation on how to install the certificate.

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
