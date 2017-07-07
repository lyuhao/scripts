#! /bin/bash
if [ -z "$1" ]
then
	exit 1
fi

LCSERVER=$1


echo "-----------starting kmeans---------------"
echo "LCSERVER=${LCSERVER}

"
/home/ds318/gitRepo/spark/bin/spark-submit --num-executors 20 --jars /home/ds318/gitRepo/spark/examples/target/scala-2.11/jars/scopt_2.11-3.3.0.jar \
--class org.apache.spark.examples.mllib.DenseKMeans --master spark://$(hostname):7077 \
--deploy-mode client \
/home/ds318/gitRepo/spark/examples/target/scala-2.11/jars/spark-examples_2.11-2.1.0.jar \
-k 1000 ~/yuhao_datasets/USCensus1990.data.txt &

echo $! > 1.pid
echo "waiting for $(cat 1.pid)"
wait $(cat 1.pid)
rm 1.pid
echo "------------kmeans finished---------"
ssh ${LCSERVER} "/home/ds318/gitRepo/tailbench/moses/kill_server.sh"

