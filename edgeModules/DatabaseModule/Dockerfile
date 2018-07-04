FROM ubuntu:xenial
MAINTAINER Sacha LHOPITAL <sacha.lhopital@viseo.com>

RUN apt-get update && \
    apt-get install -y --no-install-recommends libcurl4-openssl-dev python-pip libboost-python-dev && \
    rm -rf /var/lib/apt/lists/* 

WORKDIR /app

RUN mkdir -p /usr/src/app 
WORKDIR /usr/src/app 

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
RUN useradd -ms /bin/bash moduleuser
USER moduleuser

CMD ["python", "-u", "./main.py"]