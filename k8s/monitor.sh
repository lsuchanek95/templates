#!/bin/bash
echo -n "`date` "
if [[ ! -f '/opt/scaleout_url.txt' ]]; then
  echo "no scaleout_url.txt"
  exit 0
fi

# NODES=`kubectl get nodes|grep -v 'master'`
# TOTAL_COUNT=$((`echo "$NODES"| wc -l` - 1))
# READY_COUNT=$((`echo "$NODES"| grep 'Ready' | wc -l`))
# NOTREADY_COUNT=$((`echo "$NODES"| grep 'NotReady' | wc -l`)) 
# MEMP_COUNT=$((`echo "$NODES"|grep 'MemoryPressure' | wc -l`))
# HEALTHY_PERCENT=$((($TOTAL_COUNT-$NOTREADY_COUNT)*100/$TOTAL_COUNT))

SCALEOUT_URL=`cat /opt/scaleout_url.txt`
TOP_NODES=`kubectl top node`
if [[ -n "`echo $TOP_NODES|grep 'metric'`" ]]; then
  echo "$TOP_NODES"
  exit 0
fi

MEMS=`kubectl top node|sed -n '1!p'|awk '{print $5}'|sed 's/%//g'`
MEM_LINES=`echo $MEMS|wc -l`
SUM_MEM=`echo $MEMS |awk '{s+=$1} END {print s}'`
AVG_MEM=$(($SUM_MEM/$MEM_LINES))
echo "AVERAGE MEMORY: $AVG_MEM"

if [[ $AVG_MEM -gt 80 ]]; then
  echo "Scale out"
  curl -X POST $SCALEOUT_URL
fi
