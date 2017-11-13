#!/bin/bash

#turn off puppet agent
#sudo puppet agent --disable "running experiment"

#turn on all cores
sudo ~/scripts/bash_scripts/enable_cores.sh

#turn off core 8,9,10
#because ls application runs on core 3-7
sudo ~/scripts/bash_scripts/turnoff_cpu.sh 8 9 10

#change sudo time windows
#sudo visudo


#disable c-states
sudo ~/scripts/bash_scripts/set_cstate.sh 1 0 

#turn off turbo boost
sudo ~/scripts/bash_scripts/turbo-boost.sh disable

sudo cpupower frequency-set -f 2.10GHz
