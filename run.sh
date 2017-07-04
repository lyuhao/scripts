#! /bin/bash

SPARK_HOME=$HOME/pb_scripts/spark_scripts
ONLINE_HOME=$HOME/tailbench-v0.9/$2
# setup 
PER_COUNTER_HOME=$HOME/scripts/bash_scripts/IntelPerformanceCounterMonitorV2.8/

ssh $1 $SPARK_HOME/run_$2.sh &

echo $! > spark.pid

#$ONLINE_HOME/run_networked.sh $4 $5

#PER_COUNTER_HOME/pcm.x -csv=$1_$2_$3_$4.csv -i=300000 &

#echo $! > pcm.pid

#wait ${cat spark.pid}

#$ONLINE_HOME/kill_networked.sh

#sudo kill -9 ${cat pcm.pid}




