#! /bin/bash

SPARK_HOME=$HOME/pb_scripts/spark_scripts
ONLINE_HOME=$HOME/tailbench-v0.9/$3
# setup 
PER_COUNTER_HOME=$HOME/scripts/bash_scripts/IntelPerformanceCounterMonitorV2.8/

ssh $1 $SPARK_HOME/run_$2.sh $3 &

echo $! > spark.pid

$ONLINE_HOME/run_networked.sh $4 $5 $6 &

sudo $PER_COUNTER_HOME/pcm.x -csv=$2_$3_$5.csv -i=300000 &

echo $! > pcm.pid

#wait ${cat spark.pid}

#$ONLINE_HOME/kill_networked.sh

#sudo kill -9 ${cat pcm.pid}




