FROM ubuntu:xenial
MAINTAINER Sacha LHOPITAL <sacha.lhopital@viseo.com>

WORKDIR /app

RUN apt-get update \
	&& apt-get install -y python3-pip python3-dev 

RUN mkdir -p /usr/src/app 
WORKDIR /usr/src/app 

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .
RUN useradd -ms /bin/bash moduleuser
USER moduleuser

CMD [ "python", "-u", "./main.py" ]