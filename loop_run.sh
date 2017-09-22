#!/bin/bash

for QPS in {100..500..100}
do
	./run.sh clipper02 kmeans xapian 12,13 $QPS 1000000
	sleep 10
done
