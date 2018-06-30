FROM alpine:3.6
RUN apk update
RUN apk upgrade

RUN apk add py3-cffi
RUN apk add py3-openssl
RUN apk add py3-cryptography

RUN apk add --update py3-lxml

RUN rm -rf /var/cache/apk/*


RUN mkdir -p /usr/local/mock-idp
WORKDIR /usr/local/mock-idp

COPY requirements.txt ./
COPY bin ./bin
COPY mockidp ./mockidp
COPY doc ./doc
COPY tests ./tests

COPY mockidp.yaml .
COPY README.md .
COPY requirements.txt .
COPY setup.py .


RUN pip3 install -r requirements.txt
RUN pip3 install -e .

EXPOSE 5000

WORKDIR /

ENTRYPOINT [ "mock-idp", "-p" ]
CMD [ "5000" ]
