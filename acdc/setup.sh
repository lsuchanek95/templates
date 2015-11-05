#!/bin/bash
set -x

echo 'Install git' > /tmp/devstack
if [[ -e /etc/redhat-release ]]; then
  iptables -I INPUT -p tcp --dport 80 -j ACCEPT
  service iptables save
  yum install -y git
fi
su - stack -c 'bash /tmp/install.sh' << END
password
END
