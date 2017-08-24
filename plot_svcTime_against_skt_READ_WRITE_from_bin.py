#!/usr/bin/python


# A very rough script that takes an input bin file
# and plot service time against sockeet level 
# read and write

import numpy as np
import matplotlib.pyplot as plt
import sys
import OFFSET




input_file = str(sys.argv[1])
file = open(input_file)


svcTimes = []
sktReads = []
sktWrites = []

print "Reading data from " + input_file

with file:
	lines = file.readlines()
	for line in lines:
		times = line.split(' ')
		svcTime = int(times[OFFSET.BIN['service']])
		sktRead = int(times[OFFSET.BIN['sktRead']])
		sktWrite = int(times[OFFSET.BIN['skt1Write']])

		svcTimes.append(svcTime) #convert to ms
		sktReads.append(sktRead)
		sktWrites.append(sktWrite)
file.close()

print "Creating plots..."


print "Creating service time vs socket read  plot"
fig,ax = plt.subplots()
fig.suptitle('Service Time vs. Socket Read')
ax.plot(sktReads, svcTimes,'bo')
ax.set_xlabel('socket read (bytes)')
ax.set_ylabel('service time (ms)')
fig.savefig(input_file+'_service_vs_sktRead.jpg', dpi=1200)
plt.close(fig)

print "Creating service time vs socket write  plot"
fig,ax = plt.subplots()
fig.suptitle('Service Time vs. Socket Write')
ax.plot(sktWrites, svcTimes,'bo')
ax.set_xlabel('socket write (bytes)')
ax.set_ylabel('service time (ms)')
fig.savefig(input_file+'_service_vs_sktWrite.jpg', dpi=1200)
plt.close(fig)