#! /bin/bash
/home/yl408/spark/bin/spark-submit --num-executors 20 --jars /home/yl408/spark/examples/target/scala-2.11/jars/scopt_2.11-3.3.0.jar \
--class org.apache.spark.examples.mllib.LinearRegression --master spark://clipper04.egr.duke.edu:7077 \
--deploy-mode client \
/home/yl408/spark/examples/target/scala-2.11/jars/spark-examples_2.11-2.1.0.jar \
-k 1000 ~/yuhao_datasets/kdda &

echo $! > 1.pid

wait $(cat 1.pid)

ssh clipper03 '/home/yl408/pb_scripts/kill.sh xapian'