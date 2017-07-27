#!/bin/bash

#A simple program that sources trace_moses.sh from 100 QPS to 1000 QPS
SERVERCORES=21-23
CLIENTCORES=9-11 
MAXREQS=0

for QPS in {100..1000..100}
do
	FILENAME=q${QPS}base
	source ./trace_moses.sh ${QPS} ${SERVERCORES} ${CLIENTCORES} ${FILENAME} ${MAXREQS}
	sleep 5
done

