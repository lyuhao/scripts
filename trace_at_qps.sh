#!/bin/bash


#parameter parsing
if [ "$#" -ne 1 ]
then
        echo "Please call the with the following format:"
        echo "./loop_run.sh [QPS]"
        exit 1
fi
#arguments
QPS=$1
STARTINGCORE0=12
STARTINGCORE1=36

for numCore in {1..10..1}
do
	SPARKMAXCORE=$(( ${numCore} * 2 ))
	source ./set_worker_max_core_SPARK.sh ${SPARKMAXCORE}
	ENDINGCORE0 = $(( ${STARTINGCORE0} + ${numCore} ))
	ENDINGCORE1 = $(( ${STARTINGCORE1} + ${numCore} ))
	SPARKCORES = "${STARTINGCORE0}-${ENDINGCORE0},${STARTINGCORE1}-{ENDINGCORE1}"
	taskset -c ${SPARKCORES} \
		/home/ds318/gitRepo/spark/sbin/start-slave.sh clipper03.egr.duke.edu:7077
	sleep 10
	source ./trace_moses_spark.sh  ${QPS} 21-23 9-11 clipper03 kmeans \
		q${QPS}k${numCore} ${SPARKCORES}
	sleep 5
	source ./kill_spark_worker.sh
	sleep 3
done
