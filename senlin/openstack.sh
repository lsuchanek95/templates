#!/bin/env bash
set -x

OS_TOKEN=${OS_TOKEN:-de5a55cbef9444c3aaa539697fe74d51}
HOST_IP=9.123.137.235
KEYSTONE_V3=http://$HOST_IP:5000/v3
openstack \
        --os-token $OS_TOKEN \
        --os-url=$KEYSTONE_V3 \
        --os-identity-api-version=3 \
        $@
