#!/bin/bash
#exec 3> /dev/cpu_dma_latency
#echo -ne '\000\000\000\000' >&3
taskset -c $1 ./set_cstate $2 &
echo $! > setcstate.pid
