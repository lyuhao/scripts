#!/bin/bash

#This script is used to characterize the performance of server
#pin this to a core that is different from client and server
#sudo another command before executing to allow smooth operation

source /home/ds318/scripts/bash_helpers/readPathsConfiguration.sh

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

if [ "$#" -ne 4 ]
then 
	echo "Usage:"
	echo "${BASH_SOURCE[0]} QPS CLIENT_THREADS CLIENT_CORES SERVER_MACHINE"
	exit 1
fi


QPS=$1
CLIENT_THREADS=$2
CLIENT_CORES=$3
SERVER_MACHINE=$4

#launch client
source ${ONLINE_HOME}/launch_client.sh ${QPS} ${CLIENT_THREADS} ${CLIENT_CORES} ${SERVER_MACHINE}

sleep 5s #wait for client to dump stats
echo "moving data"
DATADIR=${SCRIPT_HOME}/server_characterization_data
cp lats.bin DATADIR/q${QPS}.bin

