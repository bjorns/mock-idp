FROM python:3.13-alpine
RUN apk update && apk upgrade

# Dev dependencies for crypto package that can be
# remove after install
RUN apk add gcc musl-dev openssl-dev libffi-dev \
  libxml2-dev libxslt-dev \
  rust cargo

# Runtime dependencies
RUN apk add libxslt

RUN mkdir -p /usr/local/mock-idp
WORKDIR /usr/local/mock-idp

RUN pip install --upgrade pip

# cryptography is the most complicated package and if
# install fails in pipenv the error message is not
# clearly understandable. So we install it separately
RUN pip install cryptography

# Copy code
COPY bin ./bin
COPY mockidp ./mockidp
COPY doc ./doc
COPY tests ./tests
COPY setup.py .
COPY README.md .

# Install repo as package
RUN pip install -e .

# Remove build tools to save some space
RUN apk del gcc musl-dev openssl-dev libffi-dev \
  libxml2-dev libxslt-dev \
  rust cargo

# Clean out alpine apk package cache
RUN rm -rf /var/cache/apk/*

EXPOSE 5000

ENTRYPOINT [ "mock-idp", "--host", "0.0.0.0", "--port" ]
CMD [ "5000" ]
