#!/bin/sh

for i in `seq 1 47`;
do
echo 1 > /sys/devices/system/cpu/cpu$i/online
done


