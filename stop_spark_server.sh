#!/bin/bash

#kill spark master
~/gitRepo/scripts/kill_spark_master.sh

#turn on turbo boost
sudo ~/gitRepo/scripts/bash_scripts/turbo-boost.sh enable

#enable c-states
sudo ~/gitRepo/scripts/bash_scripts/reset_cstate.sh 

#reset cpu gorvernor to on demand
sudo cpupower frequency-set -g ondemand


