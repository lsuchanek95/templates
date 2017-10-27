#!/bin/bash
set -x

NODES=`kubectl get nodes|grep -v 'master'`
TOTAL_COUNT=$((`echo "$NODES"| wc -l` - 1))
READY_COUNT=$((`echo "$NODES"| grep 'Ready' | wc -l`))
NOTREADY_COUNT=$((`echo "$NODES"| grep 'NotReady' | wc -l`))
MEM_COUNT=$((`echo "$NODES"|grep 'MemoryPressure' | wc -l`))

HEALTHY_PERCENT=$((($TOTAL_COUNT-$NOTREADY_COUNT)*100/$TOTAL_COUNT))


MEMS=`kubectl top  node|sed -n '1!p'|awk '{print $5}'|sed 's/%//g'`
MEM_LINES=`echo $MEMS|wc -l`
SUM_MEM=`echo $MEMS |awk '{s+=$1} END {print s}'`
AVG_MEM=$(($SUM_MEM/$MEM_LINES))
if [[ -f '/opt/scaleout_url.txt' ]] && [[ $AVG_MEM -gt 80 ]];then
  echo "alarm"
fi
