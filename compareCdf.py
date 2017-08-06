#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import os


trials = [ str(sys.argv[1]) , str(sys.argv[2]) ]

for i in range(0, len(trials)):
	if trials[i].endswith('/'):
		trials[i] = trials[i][:-1]

for trial in trials:
	if not os.path.isdir(trial):
		print "ERROR: trial " + trial  + 'not found'
		exit(1)

dirName = trials[0] + '_vs_' + trials[1]
if not os.path.isdir(dirName):
	os.mkdir(dirName)

paths = []
for trial in trials:
	paths.append(trial + '/' + trial + '.bin_cdf') 

percentiles = []
svcTimes = []
ltcTimes = []

for path in paths:
	percentiles.append([])
	svcTimes.append([])
	ltcTimes.append([])
	print "Reading data from " + path
	with open(path) as f:
		lines = f.readlines()
		for line in lines:
			times = line.split(' ')
			percentile = float(times[0])
			svcTime = float(times[1])
			ltcTime = float(times[2])

			percentiles[-1].append(percentile)
			svcTimes[-1].append(svcTime) 
			ltcTimes[-1].append(ltcTime) 

print "plotting distribution comparison"
fig,ax = plt.subplots()
fig.suptitle('Percentile vs. Time')
lineStyle = ['-', ':']
for i in range(0,len(trials)):
	ax.plot(svcTimes[i] ,percentiles[i],'g'+lineStyle[i],label=trials[i]+'SVC')
	ax.plot(ltcTimes[i] ,percentiles[i],'r'+lineStyle[i],label=trials[i]+'LTC')
ax.set_xlabel('time (ms)')
ax.set_ylabel('percentile')
plt.legend()
#plt.show()
fig.savefig(dirName+'/percentile_comparison.jpg',dpi=1200)
plt.close(fig)

