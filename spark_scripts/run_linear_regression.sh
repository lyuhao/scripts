#! /bin/bash
if [ -z "$1" ]
then
	exit 1
fi

LCSERVER=$1


echo "-----------starting linear_regression---------------"
echo "LCSERVER=${LCSERVER}"

/home/ds318/gitRepo/spark/bin/spark-submit --num-executors 20 --jars /home/ds318/gitRepo/spark/examples/target/scala-2.11/jars/scopt_2.11-3.3.0.jar \
--class org.apache.spark.examples.mllib.LinearRegression --master spark://$(hostname):7077 \
--deploy-mode client \
/home/ds318/gitRepo/spark/examples/target/scala-2.11/jars/spark-examples_2.11-2.1.0.jar \
 ~/yuhao_datasets/kdda &

echo $! > linear_regression.pid
sleep 5m
kill $( cat linear_regression.pid )
rm linear_regression.pid
echo "------------linear_regression killed---------"
ssh ${LCSERVER} "/home/ds318/gitRepo/tailbench/moses/kill_server.sh"


