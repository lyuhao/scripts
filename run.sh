#! /bin/bash
## parameter: 1. worker URL 2. spark application 3. online application 4. online core 5.QPS 6.MAX-REQ
SPARK_HOME=$HOME/pb_scripts/spark_scripts
ONLINE_HOME=$HOME/tailbench-v0.9/$3
# setup 
PER_COUNTER_HOME=$HOME/scripts/bash_scripts/IntelPerformanceCounterMonitorV2.8/

ssh $1 $SPARK_HOME/run_$2.sh &

echo $! > spark.pid

#cat spark.pid

$ONLINE_HOME/run_networked.sh $4 $5 $6 &

sudo $PER_COUNTER_HOME/pcm.x -r 0.05 -csv=$2_$3_$5.csv -i=300000 &

echo $! > pcm.pid

#cat pcm.pid

wait $(cat spark.pid)

#./kill.sh $3

sleep 1

$ONLINE_HOME/kill_networked.sh
sudo pkill -TERM -P $(cat pcm.pid)




