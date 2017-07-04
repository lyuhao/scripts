#! /bin/bash

SPARK_HOME=$HOME/summer_scripts/spark_scripts
ONLINE_HOME=$HOME/tailbench-v0.9/$1

$ONLINE_HOME/kill_networked.sh

sudo kill -9 ${cat pcm.pid}
kill -9 ${cat spark.pid}