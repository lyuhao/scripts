#!/bin/bash

#setup
SPARK_HOME=/home/ds318/gitRepo/scripts/spark_scripts
ONLINE_HOME=/home/ds318/gitRepo/tailbench/moses
PER_COUNTER_HOME=/home/ds318/bash_scripts/IntelPerformanceCounterMonitorV2.8

#check
if ! [ -d ${SPARK_HOME} ]
then
	echo "SPARK_HOME path ${SPARK_HOME} does not exist"
	exit 1
fi

if ! [ -d ${ONLINE_HOME} ]
then
        echo "ONLINE_HOME path ${ONLINE_HOME} does not exist"
        exit 1
fi

if ! [ -d ${PER_COUNTER_HOME} ]
then
        echo "PER_COUNTER_HOME path ${PER_COUNTER_HOME} does not exist"
        exit 1
fi

if [ "$#" -ne 5 ]
then
	echo "To be used on server to deploy LC Applicatoin"
	echo "Please call the with the following format:"
	echo "./run.sh [QPS SERVERCORES CLIENTCORES SERVER SPARKAPP]"
	exit 1
fi
#parameters
QPS=$1
SERVERCORES=$2
CLIENTCORES=$3
SERVER=$4
SPARKAPP=$5

WARMUPREQS=$(( 20 * ${QPS} ))

if ps -aux | grep executor | grep spark  > /dev/null
then
        echo "ERROR: another spark executor is running, exiting"       
        exit 1
fi




#disable NMI watchdog for performance counter
sudo bash -c "echo 0 > /proc/sys/kernel/nmi_watchdog"
sudo cpupower frequency-set -g performance
#start moses
taskset -c 8 ${ONLINE_HOME}/run_networked.sh 2 0 ${WARMUPREQS} ${SERVERCORES} \
				${QPS} 1 ${CLIENTCORES} &
echo $! > onlineTool.pid
#start performance counter
sudo taskset -c 24-35 $PER_COUNTER_HOME/pcm.x -csv=${SPARKAPP}_${QPS}.csv -i=300000 &
echo $! > pcm.pid

sleep 20 #wait for moses to stablize
#start spark job
ssh ${SERVER} "$SPARK_HOME/run_${SPARKAPP}.sh $(hostname)" &



wait $(cat onlineTool.pid) #wait for server to be killed by spark script

sudo kill $(cat pcm.pid)

#enable NMI watchdog
sudo bash -c "echo 1 > /proc/sys/kernel/nmi_watchdog" 
sudo cpupower frequency-set -g ondemand


