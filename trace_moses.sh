#!/bin/bash

#setup
source ./paths.sh

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


if [ "$#" -ne 5 ]
then
	echo "To be used on server to deploy LC Applicatoin"
	echo "Please call the with the following format:"
	echo "${BASH_SOURCE[0]} [QPS SERVERCORES CLIENTCORES FILENAME MAXREQS]"
	exit 1
fi

#parameters
QPS=$1
SERVERCORES=$2
CLIENTCORES=$3
FILENAME=$4
MAXREQS=$5
PCMCORES=24-35


if [ -d ${FILENAME} ]
then
        echo "ERROR: Directory ${FILENAME} already exists"
        exit 1
fi

mkdir ${FILENAME}

WARMUPREQS=$(( 20 * ${QPS} ))

#write setup
echo -e "QPS=${QPS}\nSERVERCORES=${SERVERCORES}\nCLIENTCORES=${CLIENTCORES}" | tee ${FILENAME}.setup
echo -e "FILENAME=${FILENAME}\nPCMCORES=${PCMCORES}" | tee -a ${FILENAME}.setup
echo -e "MAXREQS=${MAXREQS}" | tee -a ${FILENAME}.setup
mv ${FILENAME}.setup ${FILENAME}/.

#manipulate MAXREQS such that lats.bin ends exactly where it should
if ! [ ${MAXREQS} -eq 0 ]
then
        MAXREQS=$(( ${MAXREQS} - ${WARMUPREQS} + 1  ))
fi


#disable NMI watchdog for performance counter
sudo bash -c "echo 0 > /proc/sys/kernel/nmi_watchdog"
sudo cpupower frequency-set -g performance
sleep 5

#start performance counter
sudo taskset -c ${PCMCORES} $PER_COUNTER_HOME/pcm.x 0.05 -csv=${FILENAME}.csv &
echo $! > pcm.pid
sleep 5

#start moses
taskset -c 8 ${ONLINE_HOME}/run_networked.sh 2 ${MAXREQS} ${WARMUPREQS} ${SERVERCORES} \
				${QPS} 1 ${CLIENTCORES} &
echo $! > onlineTool.pid
echo -e "moses started at $( date +%s)" | tee ${FILENAME}.time
mv ${FILENAME}.time ${FILENAME}/.

if [ ${MAXREQS} -eq 0 ]
then
	sleep 6m
else
	wait $(cat onlineTool.pid)
fi

# kill moses
${ONLINE_HOME}/kill_server.sh
rm onlineTool.pid

sudo kill $(cat pcm.pid)
rm pcm.pid
#enable NMI watchdog
sudo bash -c "echo 1 > /proc/sys/kernel/nmi_watchdog" 
sudo cpupower frequency-set -g ondemand


while ! [ -e lats.bin ]; do
	sleep 1
done
mv lats.bin ${FILENAME}/${FILENAME}.bin

while ! [ -e ${FILENAME}.csv ]; do
	sleep 1
done
mv ${FILENAME}.csv ${FILENAME}/.

while ! [ -e test.out ]; do
        sleep 1
done
mv test.out ${FILENAME}/test.out
