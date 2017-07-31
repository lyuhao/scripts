#!/bin/bash

# A simple program that loop trace_at_qps.sh from 100 to 1000

for QPS in {100..1000..100}
do
	source ./trace_at_qps.sh ${QPS} 1
	sleep 10
done
