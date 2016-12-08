FROM tknerr/baseimage-ubuntu:14.04
MAINTAINER Mark Zaslavskiy <mark.zaslavskiy@gmail.com>
RUN apt-get update && apt-get -y install git vim 
RUN git clone https://github.com/OSLL/mooc-lp-statistics.git
RUN cd /mooc-lp-statistics && ./scripts/install_dependencies.sh 
RUN cd /mooc-lp-statistics && ./scripts/setup_pip_dependencies.sh 
RUN cd /mooc-lp-statistics && ./scripts/local_deploy.sh
RUN rm /etc/apache2/sites-enabled/000-default.conf rm /etc/apache2/sites-available/000-default.conf
RUN sed -i 's/ServerName/#/g' /etc/apache2/sites-available/mooc-lp-statistics.conf
RUN mkdir -p /data/db
RUN chown -R mongodb:mongodb /data
RUN sed -i 's/journal=true/journal=false/g' /etc/mongodb.conf
