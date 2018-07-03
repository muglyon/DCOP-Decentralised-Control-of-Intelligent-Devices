FROM ubuntu:xenial
MAINTAINER Sacha LHOPITAL <sacha.lhopital@viseo.com>

# Install MongoDB.
# RUN \
#   apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10 && \
#   echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' > /etc/apt/sources.list.d/mongodb.list && \
#   apt-get update && \
#   apt-get install -y mongodb-org && \
#   rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y --no-install-recommends libcurl4-openssl-dev python-pip libboost-python-dev && \
    rm -rf /var/lib/apt/lists/* 

# Define mountable directories.
#VOLUME ["/data/db"]

WORKDIR /app

RUN mkdir -p /usr/src/app 
WORKDIR /usr/src/app 

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
RUN useradd -ms /bin/bash moduleuser
USER moduleuser

CMD ["python", "-u", "./main.py"]