#! /bin/bash

#setup
source ./paths.sh

#check

if ! [ -d ${SPARK_HOME} ]
then
        echo "SPARK_HOME path ${SPARK_HOME} does not exist"
        exit 1
fi



if ! [ -d ${PER_COUNTER_HOME} ]
then
        echo "PER_COUNTER_HOME path ${PER_COUNTER_HOME} does not exist"
        exit 1
fi

if [ "$#" -ne 4 ] 
then
	echo "To be used run performance counter with spark job"
	echo "Please call the with the following format:"
	echo "${BASH_SOURCE[0]} [SERVER SPARKAPP FILENAME SPARKCFREQ]"
	exit 1
fi
#parameters
SERVER=$1
SPARKAPP=$2
FILENAME=$3
SPARKCFREQ=$4
PCMCORES=24-35
SPARKCORES=12-19,36-43

if [ -d ${FILENAME} ]
then
	echo "ERROR: Directory ${FILENAME} already exists"
	exit 1
fi

mkdir ${FILENAME}

#write setup
echo -e "SERVER=${SERVER}\nSPARKAPP=${SPARKAPP}" | tee ${FILENAME}.setup
echo -e "FILENAME=${FILENAME}\nPCMCORES=${PCMCORES}" | tee -a ${FILENAME}.setup
echo -e "SPARKCORES=${SPARKCORES}\nSPARKCFREQ=${SPARKCFREQ}" | tee -a ${FILENAME}.setup
mv ${FILENAME}.setup ${FILENAME}/.

#disable NMI watchdog for performance counter
sudo bash -c "echo 0 > /proc/sys/kernel/nmi_watchdog"

#change core frequency
sudo cpupower -c ${SPARKCORES} frequency-set -f ${SPARKCFREQ}GHz
sudo cpupower -c ${SPARKCORES} frequency-info

sleep 5

#start performance counter
sudo taskset -c ${PCMCORES} $PER_COUNTER_HOME/pcm.x 0.05 -csv=${FILENAME}.csv &
echo $! > pcm.pid
sleep 5

#start spark job
echo -e "spark started at $( date +%s)" | tee -a ${FILENAME}.time
ssh ${SERVER} "$SPARK_HOME/run_${SPARKAPP}.sh $(hostname)" &
mv ${FILENAME}.time ${FILENAME}/.

sleep 5m
sudo kill $(cat pcm.pid)
rm pcm.pid
#enable NMI watchdog
sudo bash -c "echo 1 > /proc/sys/kernel/nmi_watchdog" 
sudo cpupower frequency-set -g ondemand

while ! [ -e ${FILENAME}.csv ]; do
	sleep 1
done
mv ${FILENAME}.csv ${FILENAME}/.


