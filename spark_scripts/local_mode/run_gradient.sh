#!/bin/bash
taskset -c $1 ~/spark/bin/run-example org.apache.spark.examples.mllib.GradientBoostedTreesRunner ~/yuhao_datasets/kdda &
echo $! > spark.pid
