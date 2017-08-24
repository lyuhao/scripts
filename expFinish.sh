#!/bin/bash

#turn on all cores
sudo ~/scripts/bash_scripts/enable_cores.sh

#turn on turbo boost
sudo ~/scripts/bash_scripts/turbo-boost.sh enable

#disable c-states
sudo ~/scripts/bash_scripts/reset_cstate.sh 

#turn on puppet agent
#sudo puppet agent --enable


