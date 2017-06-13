# Mock IDP

Ever needed to test an SSO setup but don't have access to the IDP for whatever
reason?

Mock IDP provides a SAML2.0 IDP using POST bindings without need for a user
database or complicated enterprise software setup.

## Prerequisites

Mock-idp requires python 3.6 and pip

## Installation

    $ git clone
    $ cd mock-idp
    $ ./app

## Configuration

All system config is located in mock-idp/config.yaml


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


### Users

Users is a fairly self explanatory hardcoded list of user credentials recognized
by the IDP:

    users:
      charlie:
        first_name: "Charlie"
        last_name: "Brown"
        email: "charlie@gmail.com"
        password: snoopy
        roles:
          - administrators

## Service Provider configuration

TODO


## Compatibility

Mock-IDP has been tested with the following service providers

    * Adobe Experience Manager (AEM) 6.2
