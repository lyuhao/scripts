#!/bin/bash
#sudo ~/bash_scripts/IntelPerformanceCounterMonitorV2.8/pcm.x -r -i=1
#sudo ~/bash_scripts/IntelPerformanceCounterMonitorV2.8/pcm.x -csv=/scratch/sf117/cc_sprint.csv -i=30000 &
taskset -c $1 ~/spark/bin/run-example org.apache.spark.examples.graphx.Analytics cc ~/yuhao_datasets/part-r-00476-00478 --numEPart=72 &
echo $! > spark.pid
