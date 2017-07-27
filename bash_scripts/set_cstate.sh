#!/bin/bash

taskset -c $1 ./set_cstate $2 &
echo $! > setcstate.pid
