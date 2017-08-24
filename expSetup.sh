#!/bin/bash

#turn off puppet agent
#sudo puppet agent --disable "running experiment"

#turn on all cores
sudo ~/gitRepo/scripts/bash_scripts/enable_cores.sh

#turn off core 13,14,15
#because ls application runs on core 5-7
sudo ~/scripts/bash_scripts/turnoff_cpu.sh 13 14 15

#change sudo time windows
#sudo visudo


#disable c-states
sudo ~/scripts/bash_scripts/set_cstate.sh 1 0 

#turn off turbo boost
sudo ~/gitRepo/scripts/bash_scripts/turbo-boost.sh disable
