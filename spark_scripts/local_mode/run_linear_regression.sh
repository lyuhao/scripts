#!/bin/bash
taskset -c $1 ~/spark/bin/run-example org.apache.spark.examples.mllib.LinearRegression ~/yuhao_datasets/kdda_part &
echo $! > spark.pid
