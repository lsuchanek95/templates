#!/bin/bash -v
yum -y install httpd
systemctl start httpd.service
