#!/bin/bash
set -x

cp -f /opt/stack/heat/heat/engine/clients/os/senlin.py client/
cp -f /opt/stack/heat/heat/engine/resources/openstack/senlin/*.py resources/senlin/
cp -f /opt/stack/heat/setup.cfg ./
