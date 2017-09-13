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

if [ "$#" -ne 4 ]
then 
	echo "Usage:"
	echo "${BASH_SOURCE[0]} SERVER_THREADS MAXREQS WARMUPREQS SERVER_CORES"
	exit 1
fi

SERVER_THREADS=$1
MAXREQS=$2
WARMUPREQS=$3
SERVER_CORES=$4

#launch server
cd ${ONLINE_HOME}
source ./launch_server.sh ${SERVER_THREADS} ${MAXREQS} ${WARMUPREQS} ${SERVER_CORES}