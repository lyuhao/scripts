#! /bin/bash

#setup
source ./paths.sh

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

if [ "$#" -ne 7 ]
then
	echo "To be used on server to deploy LC Applicatoin"
	echo "Please call the with the following format:"
	echo "./trace_moses_spark.sh [QPS SERVERCORES CLIENTCORES SERVER SPARKAPP FILENAME SPARKCFREQ]"
	exit 1
fi
#parameters
QPS=$1
SERVERCORES=$2
CLIENTCORES=$3
SERVER=$4
SPARKAPP=$5
FILENAME=$6
SPARKCFREQ=$7
PCMCORES=24-35
SPARKCORES=12-19,36-43

if [ -d ${FILENAME} ]
then
	echo "ERROR: Directory ${FILENAME} already exists"
	exit 1
fi

mkdir ${FILENAME}

WARMUPREQS=$(( 20 * ${QPS} ))

#write setup
echo -e "QPS=${QPS}\nSERVERCORES=${SERVERCORES}\nCLIENTCORES=${CLIENTCORES}" | tee ${FILENAME}.setup
echo -e "SERVER=${SERVER}\nSPARKAPP=${SPARKAPP}" | tee -a ${FILENAME}.setup
echo -e "FILENAME=${FILENAME}\nPCMCORES=${PCMCORES}" | tee -a ${FILENAME}.setup
echo -e "SPARKCORES=${SPARKCORES}\nSPARKCFREQ=${SPARKCFREQ}" | tee -a ${FILENAME}.setup
mv ${FILENAME}.setup ${FILENAME}/.

#disable NMI watchdog for performance counter
sudo bash -c "echo 0 > /proc/sys/kernel/nmi_watchdog"

#change core frequency
sudo cpupower -c ${SERVERCORES},${CLIENTCORES} frequency-set -f 2.70GHz
sudo cpupower -c ${SPARKCORES} frequency-set -f ${SPARKCFREQ}GHz
sudo cpupower -c ${SERVERCORES},${CLIENTCORES},${SPARKCORES} frequency-info

sleep 5

#start performance counter
sudo taskset -c ${PCMCORES} $PER_COUNTER_HOME/pcm.x 0.05 -csv=${FILENAME}.csv &
echo $! > pcm.pid
sleep 5

#start moses
taskset -c 8 ${ONLINE_HOME}/run_networked.sh 2 0 ${WARMUPREQS} ${SERVERCORES} \
				${QPS} 1 ${CLIENTCORES} &
echo $! > onlineTool.pid

sleep 40

#start spark job
echo -e "spark started at $( date +%s)" | tee -a ${FILENAME}.time
ssh ${SERVER} "$SPARK_HOME/run_${SPARKAPP}.sh $(hostname)" &
mv ${FILENAME}.time ${FILENAME}/.


wait $(cat onlineTool.pid) #wait for server to be killed by spark script
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

