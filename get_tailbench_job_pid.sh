#!/bin/bash

#Print the pid of specified tailbench job
#process info seen in ps has to contain "tailbench"
# and the argument given

#exit on error 1 if no input is provided
#prints id if process is running, -1 if not

if [ "$#" -ne 1 ]; then
	echo "Usage: ${BASH_SOURCE[0]} TAILBENCH_JOB"
	exit 1
fi

TAILBENCH_JOB=$1

if ps -aux | grep tailbench | grep ${TAILBENCH_JOB} > /dev/null
then
	echo $(`ps -ef | grep master | grep spark | grep java | grep -v grep | awk '{print $2}'`)
else
	echo -1
fi
