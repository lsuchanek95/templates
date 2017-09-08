#!/bin/bash
echo DB_IP > /tmp/db_ip.txt 
add-apt-repository ppa:openjdk-r/ppa
apt-get update
apt-get install -y openjdk-7-jdk