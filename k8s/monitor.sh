#!/bin/bash
set -x

if [[ ! -f '/opt/scaleout_url.txt' ]]; then
  echo "`date` no scaleout_url.txt"
  exit 0
fi

# NODES=`kubectl get nodes|grep -v 'master'`
# TOTAL_COUNT=$((`echo "$NODES"| wc -l` - 1))
# READY_COUNT=$((`echo "$NODES"| grep 'Ready' | wc -l`))
# NOTREADY_COUNT=$((`echo "$NODES"| grep 'NotReady' | wc -l`)) 
# MEMP_COUNT=$((`echo "$NODES"|grep 'MemoryPressure' | wc -l`))
# HEALTHY_PERCENT=$((($TOTAL_COUNT-$NOTREADY_COUNT)*100/$TOTAL_COUNT))

SCALEOUT_URL=`cat /opt/scaleout_url.txt`

MEMS=`kubectl top  node|sed -n '1!p'|awk '{print $5}'|sed 's/%//g'`
MEM_LINES=`echo $MEMS|wc -l`
SUM_MEM=`echo $MEMS |awk '{s+=$1} END {print s}'`
AVG_MEM=$(($SUM_MEM/$MEM_LINES))

if [[ $AVG_MEM -gt 80 ]]; then
  echo -n "`date` "
  echo "AVERAGE MEMORY: $AVG_MEM"
  curl -X POST $SCALEOUT_URL
fi
