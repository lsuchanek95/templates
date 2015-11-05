#!/bin/bash
set -x

cd /opt/stack/
echo "Clone devstack" > /tmp/install_devstack
git clone https://github.com/openstack-dev/devstack
cp /tmp/local.conf /opt/stack/devstack/
cd /opt/stack/devstack
bash -x ./stack.sh 2>&1 |tee -a /tmp/install_devstack
