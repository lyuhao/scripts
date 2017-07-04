#! /bin/bash
/home/yl408/spark/bin/spark-submit --num-executors 20 --jars /home/yl408/spark/examples/target/scala-2.11/jars/scopt_2.11-3.3.0.jar \
--class org.apache.spark.examples.graphx.LiveJournalPageRank --master spark://clipper04.egr.duke.edu:7077 \
--deploy-mode client \
/home/yl408/spark/examples/target/scala-2.11/jars/spark-examples_2.11-2.1.0.jar \  
/home/yl408/yuhao_datasets/40 --numEPart=72 &

echo $! > 1.pid

wait ${cat 1.pid}

ssh clipper04 '/home/yl408/pg_scripts/kill.sh'
