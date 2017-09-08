#!/bin/bash
echo "DB_IP db_server" >> /etc/hosts
add-apt-repository ppa:openjdk-r/ppa
apt-get update
apt-get install -y openjdk-7-jdk