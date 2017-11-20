#!/bin/bash

NIC_NAME=`ip route |grep default|awk '{print $5}'`
NET_INFO=`ip a |grep $NIC_NAME|grep inet|awk '{print $2}'`
IP=`echo $NET_INFO|cut -d'/' -f1`
PREFIX=`echo $NET_INFO|cut -d'/' -f2`
GATEWAY=`ip route |grep default|awk '{print $3}'`

sed -i "2i IPADDR=$IP" /etc/sysconfig/network-scripts/ifcfg-$NIC_NAME
sed -i "2i PREFIX=$PREFIX" /etc/sysconfig/network-scripts/ifcfg-$NIC_NAME
sed -i "2i GATEWAY=$GATEWAY" /etc/sysconfig/network-scripts/ifcfg-$NIC_NAME
sed -i 's/^BOOTPROTO=.*/BOOTPROTO=none/' /etc/sysconfig/network-scripts/ifcfg-$NIC_NAME