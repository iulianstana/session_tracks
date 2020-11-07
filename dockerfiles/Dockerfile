FROM python:3.7.5-alpine

RUN pip install --upgrade pip

ADD requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000

# Create working directory
RUN mkdir /opt/session-tracks
WORKDIR /opt/session-tracks
