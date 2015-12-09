#!/usr/bin/env bash
set -x
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
curl -O https://raw.githubusercontent.com/lynic/config/master/devstack/local.conf
