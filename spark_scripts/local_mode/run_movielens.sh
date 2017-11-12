#!/bin/bash
#sudo ~/bash_scripts/IntelPerformanceCounterMonitorV2.8/pcm.x -r -i=1
#sudo ~/bash_scripts/IntelPerformanceCounterMonitorV2.8/pcm.x -csv=/scratch/sf117/als_nonsprint.csv -i=30000 &
taskset -c $1 ~/spark/bin/run-example org.apache.spark.examples.mllib.MovieLensALS   ~/yuhao_datasets/ratings.csv  &
echo $! > spark.pid
