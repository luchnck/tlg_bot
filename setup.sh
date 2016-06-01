#!/bin/bash
sudo yum update
sudo mv nginx.repo /etc/yum.repos.d/

echo installing nginx...
sudo yum install nginx

echo installing openssl...
sudo yum install openssl

echo add keys and repo for postgresql-95...
sudo  wget http://ftp.unicamp.br/pub/postgresql/repos/yum/RPM-GPG-KEY-PGDG-95 > /etc/pki/rpm-gpg/RPM-GPG-KEY-PGDG-95
sudo ln -s pgdg-95-redhat.repo /etc/yum.repos.d/pgdg-95-redhat.repo
sudo yum install postgresql95-server postresql95 postgresql-contrib



sudo ln -sf tornado.conf /etc/nginx/conf.d/tornado.conf  

sudo ln -sf qa_bot_company.pem /etc/ssh/qa_bot_company.pem

sudo wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo pip install tornado
sudo pip install psycopg2
sudo pip install momoko

