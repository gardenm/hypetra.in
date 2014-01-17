#!/usr/bin/env bash

apt-get update

apt-get -y install git-core
apt-get -y install vim
apt-get -y install build-essential checkinstall

apt-get -y install python-dev
apt-get -y install python-pip

pip install requests==2.1.0
pip install beautifulsoup4==4.3.2
