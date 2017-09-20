#!/bin/bash
taskset -c $1 ~/spark/bin/run-example org.apache.spark.examples.graphx.Analytics triangles ~/yuhao_datasets/part-r-00476-00478 --numEPart=72 &
echo $! > spark.pid
