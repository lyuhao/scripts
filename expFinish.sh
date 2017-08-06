#!/bin/bash

#turn off turbo boost
sudo ~/gitRepo/scripts/bash_scripts/turbo-boost.sh enable

#disable c-states
sudo ~/gitRepo/scripts/bash_scripts/reset_cstate.sh 

#turn on puppet agent
sudo puppet agent --enable


