FROM ubuntu:latest

FROM python:3

RUN apt-get update -qy \
	&& apt-get install -qy python3 python3-dev python3-pip python3-setuptools python3-wheel build-essential git \
	&& apt-get clean


WORKDIR /fbdownloader

ADD . /fbdownloader

RUN ls -la
RUN pip install -r requirements.txt

RUN adduser --disabled-password --gecos '' coneser
