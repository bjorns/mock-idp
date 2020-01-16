# Mock IDP

Ever needed to test an SSO setup but don't have access to the IDP for whatever
reason?

Mock IDP provides a SAML2.0 IDP using POST bindings without need for a user
database or complicated enterprise software setup.

## Prerequisites

Mock-idp requires python 3.6 and pip

## Run from source

    $ git clone
    $ cd mock-idp
    $ ./bin/mock-idp
    ...

## Pip installation

    $ pip install mock-idp
    $ mock-idp
    ...

## Configuration

All system config is located in mockidp/resources/default_config.yaml.

### Service providers

For each service provider (client) that uses the idp an entry in the service
providers session is needed. It has two values

    service_providers:
      - name: "local:aem:author"
        response_url: "http://localhost:14502/saml_login"


* **name** is the service provider entity id that the service provider sends which
    each request.
* **response_url** is the public url of the service provider. The client web
    browser will make access this so if you are running the service inside
    a virtual machine the address only needs to be accessible to the browser.

#### Certificate keys

To generate a service provider Certificate
    $ openssl genrsa -out saml.pem 2048 # Generate private key
    $ openssl req -new -key saml.pem -out saml.csr
    $ openssl x509 -req -days 365 -in saml.csr -signkey saml.pem -out saml.crt

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

### Import local config into a docker container

Provided you have produced your config file containing service providers and user account information. You can inject into a docker container by the following:

    $ docker run -p 5000:5000 -v <absolute path to your config>.yaml:/usr/local/mock-idp/mockidp/resources/default_config.yaml bjornskoglund/mock-idp:0.2.1

Copy the *cert/cert.pem* file into your Service Provider (_SP_), and be sure that the _ISSUER_ (entity id) provided by the _SP_ matches the _name:_ of the Service Provider in your config.

## Configuring a generic Service Provider

* Mock-IDP supports the POST binding protocol of SAML2.0.
* By default mock-idp runs on port 5000 and the binding path is /saml.
* the response message provides four attributes:
    - uid: The username
    - email: the user email address
    - firstName: The users first name
    - lastName: The users last name
* The logout path is /saml/logout


## Compatibility

Mock-IDP has been tested with the following service providers

* Adobe Experience Manager (AEM) 6.2
* Node.js - [saml2-js](https://www.npmjs.com/package/saml2-js) package
