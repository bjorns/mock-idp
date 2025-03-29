saml/private-key.pem:
	openssl genrsa -out $@ 2048

saml/service-provider.csr: saml/private-key.pem
	openssl req -new -key $< -out $@ -subj "/C=US/ST=New York/L=New York City/O=Some Org/OU=Some Department/CN=example.com/emailAddress=charlies@peanuts.com"

saml/service-provider.crt: saml/service-provider.csr saml/private-key.pem
	openssl x509 -req -days 365 -in $< -signkey saml/private-key.pem -out $@

certs: saml/service-provider.crt


.PHONY: certs
