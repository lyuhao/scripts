#!/bin/bash
#sudo ~/bash_scripts/IntelPerformanceCounterMonitorV2.8/pcm.x -r -i=1
#sudo ~/bash_scripts/IntelPerformanceCounterMonitorV2.8/pcm.x -csv=/scratch/sf117/naive_bayesian_nonsprint.csv -i=30000 &
taskset -c $1 ~/spark/bin/run-example org.apache.spark.examples.mllib.SparseNaiveBayes  ~/yuhao_datasets/kdda_part &>spark.out &
echo $! > spark.pid
