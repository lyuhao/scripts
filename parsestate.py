#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import csv 

input_file = sys.argv[1]
file = open(input_file)
service_time_list = list()
latency_time_list = list()
start_time_list = list()
reqlens = list()
queuelens = list()
sertime_list = list()
action_list = list()
reward_list = list()
with file:
	lines = file.readlines()
	for line in lines:
		values = line.split(' ')
		action = float(values[2][0:3])
		ql = int(values[0])
		sertime = float(values[1])
		sertime_list.append(sertime)
		queuelens.append(ql)
		action_list.append(action)
		reward_list.append(int(values[2][3:-1]))


t = range(0,len(queuelens))

fig, ax = plt.subplots(4)

ax[0].plot(t,queuelens,'r')
ax[0].set_ylabel('queue length',color = 'r')

ax[1].plot(t,sertime_list,'r')
ax[1].set_ylabel('service time',color = 'r')

ax[2].plot(t,action_list)
ax[2].set_ylabel('action',color='black')

ax[3].plot(t,reward_list)
ax[3].set_ylabel('action',color='black')


plt.show()

