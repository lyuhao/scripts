#! /bin/bash

#setup
ONLINE_HOME=/home/ds318/gitRepo/tailbench/moses
PER_COUNTER_HOME=/home/ds318/bash_scripts/IntelPerformanceCounterMonitorV2.8

#check
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

if [ "$#" -ne 4 ]
then
	echo "To be used on server to deploy LC Applicatoin"
	echo "Please call the with the following format:"
	echo "./run.sh [QPS SERVERCORES CLIENTCORESi FILENAME]"
	exit 1
fi
#parameters
QPS=$1
SERVERCORES=$2
CLIENTCORES=$3
FILENAME=$4
PCMCORES=24-35


WARMUPREQS=$(( 20 * ${QPS} ))

#write setup
echo -e "QPS=${QPS}\nSERVERCORES=${SERVERCORES}\nCLIENTCORES=${CLIENTCORES}" | tee ${FILENAME}.setup
echo -e "FILENAME=${FILENAME}\nPCMCORES=${PCMCORES}" | tee -a ${FILENAME}.setup


#disable NMI watchdog for performance counter
sudo bash -c "echo 0 > /proc/sys/kernel/nmi_watchdog"
sudo cpupower frequency-set -g performance
sleep 5

#start performance counter
sudo taskset -c ${PCMCORES} $PER_COUNTER_HOME/pcm.x 0.1 -csv=${FILENAME}.csv &
echo $! > pcm.pid
sleep 5

#start moses
taskset -c 8 ${ONLINE_HOME}/run_networked.sh 2 0 ${WARMUPREQS} ${SERVERCORES} \
				${QPS} 1 ${CLIENTCORES} &
echo $! > onlineTool.pid
echo -e "moses started at $( date )" | tee ${FILENAME}.time

sleep 17m

# kill moses
${ONLINE_HOME}/kill_server.sh
rm onlineTool.pid

sudo kill $(cat pcm.pid)
rm pcm.pid
#enable NMI watchdog
sudo bash -c "echo 1 > /proc/sys/kernel/nmi_watchdog" 
sudo cpupower frequency-set -g ondemand


while ![ -e lats.bin ]; do
	sleep 1
done

mv lats.bin ./${FILENAME}.bin
