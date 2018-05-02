FROM ubuntu:14.04
MAINTAINER Azure App Service Container Images <appsvc-images@microsoft.com>

# Python Environment
RUN apt-get update \
	&& apt-get install -y python3-pip python3-dev

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
ADD . /code/

# SSH
ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
	&& apt-get install -y --no-install-recommends openssh-server \
	&& echo "$SSH_PASSWD" | chpasswd

COPY sshd_config /etc/ssh/
	
EXPOSE 8000 2222

WORKDIR /code/app