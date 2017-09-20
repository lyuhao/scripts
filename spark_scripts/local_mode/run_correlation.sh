#!/bin/bash
#sudo ~/bash_scripts/IntelPerformanceCounterMonitorV2.8/pcm.x -r -i=1
#sudo ~/bash_scripts/IntelPerformanceCounterMonitorV2.8/pcm.x -csv=/scratch/sf117/correlation_sprint.csv -i=30000 &
taskset -c $1 ~/spark/bin/run-example org.apache.spark.examples.mllib.Correlations --input ~/yuhao_datasets/kdda &
echo $! > correlation.pid

