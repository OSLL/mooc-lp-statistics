FROM tknerr/baseimage-ubuntu:14.04
MAINTAINER Mark Zaslavskiy <mark.zaslavskiy@gmail.com>
RUN apt-get update && apt-get -y install git 
RUN ls && git clone https://github.com/OSLL/mooc-lp-statistics.git
RUN cd /mooc-lp-statistics && ./scripts/install_dependencies.sh 
RUN cd /mooc-lp-statistics && ./scripts/setup_pip_dependencies.sh 
RUN cd /mooc-lp-statistics && ./scripts/local_deploy.sh
