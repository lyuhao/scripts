#!/bin/bash

#setup
SPARK_DIR=/home/ds318/gitRepo/spark


if [ $# -ne 1 ]
then
	echo "Usage: set_worker_max_core_SPARK.sh [NUMCORE]"
	exit 1
fi 

NUMCORE=$1

if ! [ -d ${SPARK_DIR} ]
then
	echo "Spark directory ${SPARK_DIR} does not exist"
	exit 1
fi

SPARKCONF=${SPARK_DIR}/conf/spark-defaults.conf

if ! [ -e ${SPARKCONF} ]
then
	echo "Spark configuration ${SPARKCONF} does not exist"
	exit 1
fi

sed -i -e "s/.*spark.cores.max.*/spark.cores.max                                                 ${NUMCORE=}/" ${SPARKCONF}


