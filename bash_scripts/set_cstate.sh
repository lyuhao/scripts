#!/bin/bash

if [ $# -ne 2 ]
then
	echo "Usage: ${BASH_SOURCE[0]} [core latency]"
	exit 1
fi
CORE=$1
LATENCY=$2
taskset -c ${CORE} ./set_cstate ${LATENCY} &
echo $! > setcstate.pid
