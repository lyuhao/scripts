#!/bin/bash

if ps -aux | grep SparkSubmit | grep spark | grep java  > /dev/null
then
	echo spark job detected, killing
	kill -9 `ps -ef | grep SparkSubmit | grep spark | grep java | grep -v grep | awk '{print $2}'`
else
	echo no spark job detected
fi
