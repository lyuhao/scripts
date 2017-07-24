#!/bin/bash

if ps -aux | grep worker | grep spark | grep java  > /dev/null
then
	echo spark worker detected, killing
	kill -9 `ps -ef | grep worker | grep spark | grep java | grep -v grep | awk '{print $2}'`
else
	echo no spark worker detected
fi
