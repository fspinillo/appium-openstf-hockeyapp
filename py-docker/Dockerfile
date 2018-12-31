FROM python:2.7-slim-jessie

RUN apt-get -qqy update && apt-get -qqy install curl

COPY . /app
RUN pip install -q -r /app/requirements.txt

WORKDIR /app
