#!/bin/bash

#turn on all cores
sudo ~/gitRepo/scripts/bash_scripts/enable_cores.sh

#disable c-states
sudo ~/gitRepo/scripts/bash_scripts/set_cstate.sh 1 0 

#turn off turbo boost
sudo ~/gitRepo/scripts/bash_scripts/turbo-boost.sh disable

#go into spark folder and start spark master
cd ~/gitRepo/spark
./sbin/start-master.sh
