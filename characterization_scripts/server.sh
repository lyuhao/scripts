#!/bin/bash

#This scripts is used to launch the server of moses

source /home/ds318/scripts/bash_helpers/readPathsConfiguration.sh

if ! [ -d ${ONLINE_HOME} ]
then
        echo "ONLINE_HOME path ${ONLINE_HOME} does not exist"
        exit 1
fi

if [ "$#" -ne 3 ]
then 
	echo "Usage:"
	echo "${BASH_SOURCE[0]} SERVER_THREADS MAXREQS WARMUPREQS"
	exit 1
fi

SERVER_THREADS=$1
MAXREQS=$2
WARMUPREQS=$3

source ${ONLINE_HOME}/../configs.sh

BINDIR=${ONLINE_HOME}/bin

# Setup
cp ${ONLINE_HOME}/moses.ini.template ${ONLINE_HOME}/moses.ini
sed -i -e "s#@DATA_ROOT#$DATA_ROOT#g" ${ONLINE_HOME}/moses.ini

# Launch Server
TBENCH_MAXREQS=${TBENCH_MAXREQS} TBENCH_WARMUPREQS=${TBENCH_WARMUPREQS} TBENCH_NCLIENTS=1 \
TBENCH_SERVER=$(hostname) \
${BINDIR}/moses_server_networked \
    -config ${ONLINE_HOME}/moses.ini \
    -input-file ${DATA_ROOT}/moses/testTerms \
    -threads ${SERVER_THREADS} -num-tasks 7500000 -verbose 0 &

echo $! > moses_server.pid

sudo chrt -r -p 99 $(cat moses_server.pid)
