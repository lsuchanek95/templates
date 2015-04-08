#!/bin/bash
set -x

export MYSQL_ROOT_PW=Passw0rd
export MYSQL_SENLIN_PW=senlin

/home/elynn/source/senlin/tools/senlin-db-recreate
