#!/bin/bash
taskset -c $1 ~/spark/bin/run-example org.apache.spark.examples.mllib.FPGrowthExample ~/yuhao_datasets/webdocs.dat &
echo $! > spark.pid
