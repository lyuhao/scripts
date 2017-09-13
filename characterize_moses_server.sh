#!/bin/bash

#This script is used to characterize the performance of server
#pin this to a core that is different from client and server
#sudo another command before executing to allow smooth operation

source ./bash_helpers/readPathsConfiguration.sh

if ! [ -d ${ONLINE_HOME} ]
then
        echo "ONLINE_HOME path ${ONLINE_HOME} does not exist"
        exit 1
fi

if ! [ -d ${SCRIPT_HOME} ]
then
        echo "SCRIPT_HOME path ${SCRIPT_HOME} does not exist"
        exit 1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

SERVER_THREADS=$1
SERVER_CORES=$2
SERVER_MACHINE=$(hostname)
LAUNCH_SERVER_SCRIPT_CORE=4

CLIENT_MACHINE=bcl15-cmp-01.egr.duke.edu
LAUNCH_CLIENT_SCRIPT_CORE=4
CLIENT_CORES=5-7
CLIENT_THREADS=1

for QPS in {100..1000..50}
do
	MAXREQS=$((400 * ${QPS}))
	WARMUPREQS=$((50 * ${QPS}))
	#launch server
	cd ${ONLINE_HOME}
	sudo taskset -c ${LAUNCH_SERVER_SCRIPT_CORE} \
		./launch_server.sh ${SERVER_THREADS} ${MAXREQS} ${WARMUPREQS} ${SERVER_CORES} &
	echo $! > server.pid
	sleep 5s #wait for server to start up

	#launch client
	ssh ds318@${CLIENT_MACHINE} "${sudo taskset -c ${LAUNCH_CLIENT_SCRIPT_CORE} ${ONLINE_HOME}/launch_client.sh ${QPS} ${CLIENT_THREADS} ${CLIENT_CORES} ${SERVER_MACHINE}" &

	# wait for server to finish
	wait $(cat server.pid)
	rm server.pid
	sleep 10s #wait for client to dump stats

	DATADIR=${SCRIPT_HOME}/server_characterization_data/Thread${SERVER_THREADS}/QPS${QPS}
	ssh ds318@${CLIENT_MACHINE} "mkdir ${DATADIR}"
	ssh ds318@${CLIENT_MACHINE} "cp lats.bin DATADIR/q${QPS}.bin"
done
