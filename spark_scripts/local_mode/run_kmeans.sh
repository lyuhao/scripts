#!/bin/bash
taskset -c $1 ~/spark/bin/run-example org.apache.spark.examples.mllib.DenseKMeans  -k 1000 ~/yuhao_datasets/USCensus1990.data.txt &
echo $! > spark.pid
