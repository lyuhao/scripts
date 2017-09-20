#!/bin/bash
taskset -c $1 ~/spark/bin/run-example org.apache.spark.examples.mllib.BinaryClassification ~/yuhao_datasets/kdda --algorithm SVM --regType L2 --regParam 1.0 &
echo $! >spark.pid
