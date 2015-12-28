#!/bin/bash
set -x

OUTPUT=${1:-'/tmp/output.log'}
VENV='.venv'

if [[ ! -d $VENV ]];then
    virtualenv -p python3 $VENV
    source $VENV/bin/activate
    pip install -r requirements.txt
else
    source $VENV/bin/activate
fi

python test.py |tee $OUTPUT
deactivate
