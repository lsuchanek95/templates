#!/bin/bash

PARAM="\
image=vodafone-080715;\
flavor=m1.small;\
key_name=vodafone-key;\
web_security_group=web-sg;\
app_security_group=app-sg;\
db_security_group=db-sg;\
az1=nova:test140.sce.ibm.com;\
az2=nova:test141.sce.ibm.com;\
az1_web_network=yellow_az1;\
az2_web_network=yellow_az2;\
az1_app_network=red_az1;\
az2_app_network=red_az2;\
subnet=172.17.228.0/25"

heat stack-create $1 \
	--template-file=elynn_3tier.yaml \
	--parameters=$PARAM

