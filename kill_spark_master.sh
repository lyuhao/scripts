#!/bin/bash

if ps -aux | grep master | grep spark | grep java  > /dev/null
then
	echo spark master detected, killing
	kill -9 `ps -ef | grep master | grep spark | grep java | grep -v grep | awk '{print $2}'`
else
	echo no spark master detected
fi
