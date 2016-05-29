#!/bin/bash
sudo yum update
sudo mv nginx.repo /etc/yum.repos.d/

sudo yum install nginx
sudo yum install openssl

sudo ln -sf tornado.conf /etc/nginx/conf.d/tornado.conf  

sudo ln -sf qa_bot_company.pem /etc/ssh/qa_bot_company.pem

sudo wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo pip install tornado

