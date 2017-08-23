#!/bin/bash

#turn off puppet agent
sudo puppet agent --disable "running experiment"

#turn on all cores
sudo ~/gitRepo/scripts/bash_scripts/enable_cores.sh

#turn off core 45,46,47
#because ls application runs on core 21-23
sudo ~/gitRepo/scripts/bash_scripts/turnoff_cpu.sh 45 46 47

#change sudo time windows
sudo visudo


#disable c-states
sudo ~/gitRepo/scripts/bash_scripts/set_cstate.sh 1 0 

#turn off turbo boost
sudo ~/gitRepo/scripts/bash_scripts/turbo-boost.sh disable
