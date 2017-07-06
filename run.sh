#! /bin/bash

#setup
SPARK_HOME=$HOME/gitRepo/scripts/spark_scripts
ONLINE_HOME=$HOME/gitRepo/tailbench/moses
PER_COUNTER_HOME=$HOME/bash_scripts/IntelPerformanceCounterMonitorV2.8

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

if [ "$#" -ne 6 ]
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
#disable NMI watchdog for performance counter
sudo bash -c "echo 0 > /proc/sys/kernel/nmi_watchdog"

#start moses
$ONLINE_HOME/run_networked.sh 2 0 ${WARMUPREQS} ${SERVERCORES} \
				${QPS} 1 ${CLIENTCORES} &
#start performance counter
sudo $PER_COUNTER_HOME/pcm.x -csv=$2_$3_$5.csv -i=300000 &
echo $! > pcm.pid

sleep 20 #wait for moses to stablize
#start spark job
ssh ${SERVER} $SPARK_HOME/run_${SPARKAPP}.sh $(hostname) &



wait $(cat $ONLINE_HOME/server.pid) #wait for server to be killed by spark script

sudo kill -9 ${cat pcm.pid}

#enable NMI watchdog
sudo bash -c "echo 1 > /proc/sys/kernel/nmi_watchdog" 



