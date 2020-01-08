#!/bin/sh

sudo yum -y install httpd php
sudo chkconfig httpd on
sudo systemctl start httpd.service
sudo cd /var/www/html
sudo wget https://s3-us-west-2.amazonaws.com/us-west-2-aws-training/awsu-spl/spl-03/scripts/examplefiles-elb.zip
sudo unzip examplefiles-elb.zip
