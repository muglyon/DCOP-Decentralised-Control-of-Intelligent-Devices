FROM ubuntu:xenial

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends libcurl4-openssl-dev python-pip libboost-python-dev libglib2.0-0 libsm6 libxrender1 libjpeg8-dev libgtk2.0-dev libatlas-base-dev gfortran && \
    rm -rf /var/lib/apt/lists/* 

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

RUN useradd -ms /bin/bash moduleuser
USER moduleuser

CMD [ "python", "-u", "./main.py" ]