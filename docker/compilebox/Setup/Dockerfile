FROM ubuntu

RUN echo "deb http://archive.ubuntu.com/ubuntu trusty main universe" > /etc/apt/sources.lis

RUN apt-get -y update

# installing languages supported by judge | c, cpp, python2, python3, java  |  will add go later

RUN apt-get install -y gcc
RUN apt-get install -y g++
RUN apt-get install -y python
RUN apt-get install -y python3
RUN apt-get install -y golang-go

# preparing for java

RUN apt-get install -y python-software-properties
RUN apt-get install -y software-properties-common


RUN apt-add-repository -y ppa:webupd8team/java
RUN apt-get update
RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
RUN apt-get install -y oracle-java8-installer



RUN apt-get install -y mysql-server

RUN apt-get install -y sudo
RUN apt-get install -y bc

RUN echo "mysql ALL = NOPASSWD: /usr/sbin/service mysql start" | cat >> /etc/sudoers