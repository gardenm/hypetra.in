#!/usr/bin/env bash

apt-get update

apt-get -y install git-core
apt-get -y install vim
apt-get -y install build-essential checkinstall
apt-get -y install curl

apt-get -y install python-dev
apt-get -y install python-pip
apt-get -y install sqlite3 libsqlite3-dev

apt-get install -y apache2
rm -rf /var/www
ln -fs /vagrant/www /var/www

pip install requests==2.1.0
pip install beautifulsoup4==4.3.2
pip install Flask==0.10.1
pip install Flask-SQLAlchemy==1.0
pip install SQLAlchemy==0.9
pip install pysqlite==2.6.3
pip install Flask-WTF
pip install rfc3987
pip install django==1.6.2
easy_install django-tastypie
