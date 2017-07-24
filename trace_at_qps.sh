#!/bin/bash


#parameter parsing
if [ "$#" -ne 2 ]
then
        echo "Please call the with the following format:"
        echo "./loop_run.sh [QPS NUMCORESTART]"
        exit 1
fi
#arguments
QPS=$1
NUMCORESTART=$2
STARTINGCORE0=12
STARTINGCORE1=36

for (( numCore=${NUMCORESTART}; numCore<=9; numCore++ )) 
do
	SPARKMAXCORE=$(( ${numCore} * 2 ))
	source ./set_worker_max_core_SPARK.sh ${SPARKMAXCORE}
	ENDINGCORE0=$(( ${STARTINGCORE0} + ${numCore} - 1 ))
	ENDINGCORE1=$(( ${STARTINGCORE1} + ${numCore} - 1 ))
	if [ ${numCore} -eq 1 ]
	then
		SPARKCORES="${STARTINGCORE0},${STARTINGCORE1}"
	else
		SPARKCORES="${STARTINGCORE0}-${ENDINGCORE0},${STARTINGCORE1}-${ENDINGCORE1}"
	fi
	taskset -c ${SPARKCORES} \
		/home/ds318/gitRepo/spark/sbin/start-slave.sh clipper03.egr.duke.edu:7077
	sleep 10
	source ./trace_moses_spark.sh  ${QPS} 21-23 9-11 clipper03 kmeans \
		q${QPS}k${numCore} ${SPARKCORES}
	sleep 5
	source ./kill_spark_worker.sh
	sleep 3
done
