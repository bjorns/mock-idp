# Mock IDP

Ever needed to test an SSO setup but don't have access to the IDP for whatever
reason?

Mock IDP provides a SAML2.0 IDP using POST bindings without need for a user
database or complicated enterprise software setup.

## Prerequisites

Mock-idp requires python 3.6 and pip


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

## Running using Docker

### Import local config into a docker container

Provided you have produced your config file containing service providers and 
user account information. You can inject into a docker container by the
following:

    $ docker run -p 5000:5000 -v <absolute path to your config>.yaml:/usr/local/mock-idp/mockidp/resources/default_config.yaml bjornskoglund/mock-idp:0.2.1

Copy the *cert/cert.pem* file into your Service Provider (_SP_), and be sure
that the _ISSUER_ (entity id) provided by the _SP_ matches the _name:_ of the
Service Provider in your config.


## Development

Install dependencies with pip

    $ pip3 install -r requirements.txt

Run from source:

    $ git clone
    $ cd mock-idp
    $ ./bin/mock-idp
    ...

All system config is located in mockidp/resources/default_config.yaml.


## Compatibility

Mock-IDP has been tested with the following service providers

* Adobe Experience Manager (AEM) 6.2
* Node.js - [saml2-js](https://www.npmjs.com/package/saml2-js) package
