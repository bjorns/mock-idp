FROM python:3.6

RUN mkdir -p /usr/local/mock-idp
WORKDIR /usr/local/mock-idp

COPY requirements.txt ./
COPY . .

RUN pip3 install -r requirements.txt
RUN pip3 install -e .

EXPOSE 5000

WORKDIR /

CMD [ "mock-idp" ]
