#!/bin/bash

#This script is used to characterize the performance of server
#pin this to a core that is different from client and server
#sudo another command before executing to allow smooth operation

source /home/ds318/bash_helpers/readPathsConfiguration.sh

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

if [ "$#" -ne 2 ]
then 
	echo "Usage:"
	echo "${BASH_SOURCE[0]} SERVER_THREADS SERVER_CORES"
	exit 1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

SERVER_THREADS=$1
SERVER_CORES=$2
SERVER_MACHINE=bcl15-cmp-00.egr.duke.edu
LAUNCH_SERVER_SCRIPT_CORE=4

CLIENT_MACHINE=bcl15-cmp-01.egr.duke.edu
LAUNCH_CLIENT_SCRIPT_CORE=4
CLIENT_CORES=5-7
CLIENT_THREADS=1

for QPS in {100..1000..50}
do
	#launch server
	MAXREQS=$((400 * ${QPS}))
	WARMUPREQS=$((50 * ${QPS}))
	echo "--Starting server on ${SERVER_MACHINE}"
	ssh ds318@${SERVER_MACHINE} \
		"sudo taskset -c ${LAUNCH_SERVER_SCRIPT_CORE} ${SCRIPT_HOME}/characterization_scripts/server.sh ${SERVER_THREADS} ${MAXREQS} ${WARMUPREQS} ${SERVER_CORES}" &
	sleep 5s #wait for server to start up

	#launch client
	echo "--Starting client on ${CLIENT_MACHINE}" 
	ssh ds318@${CLIENT_MACHINE} \
		"sudo taskset -c ${LAUNCH_CLIENT_SCRIPT_CORE} ${SCRIPT_HOME}/characterization_scripts/client.sh ${QPS} ${CLIENT_THREADS} ${CLIENT_CORES} ${SERVER_MACHINE}" &

	sleep 5s
	echo "--Waiting for client..."
	wait $!
	echo "--QPS = ${QPS} completed"
done
