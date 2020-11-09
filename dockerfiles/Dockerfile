FROM python:3.7-alpine

RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev 

RUN pip install --upgrade pip

ADD requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONPATH PYTHONPATH:/opt/session-tracks
EXPOSE 8000

# Create working directory
RUN mkdir /opt/session-tracks
WORKDIR /opt/session-tracks
