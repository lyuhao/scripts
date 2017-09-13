#!/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
import sys
import helpers



saving = False
if '-s' in sys.argv:
	saving = True
	sys.argv.remove('-s')

trial = sys.argv[1]
binPath = trial + '/' + trial + '.bin'
interval = 50e6 #50ms, converting to ns

with open(binPath, 'r') as binFile:
	lines = binFile.readlines()
	startingTime = float(lines[0].strip().split()[1])
	endingTime = float(lines[-1].strip().split()[1]) + float(lines[-1].strip().split()[4])
	print 'Starting Time: ' + str(startingTime)
	print 'Ending Time: ' + str(endingTime)
	intervalStarts = np.arange(startingTime,endingTime,interval).tolist()
	intervalLtcs = [ [] for _ in xrange(len(intervalStarts)) ]
	for line in lines:
		datas = line.strip().split()
		reqGenTime = float(datas[1])
		reqLtcTime = float(datas[4])
		reqFinTime = reqGenTime + reqLtcTime
		elapsedTime = reqFinTime - startingTime
		intervalIndex = int(elapsedTime / interval)
		intervalLtcs[intervalIndex].append(reqLtcTime)
elapsedMid = []
interval95th = []
for i in range(0,len(intervalStarts)):
	p95 = helpers.get95th(intervalLtcs[i])
	if p95 > 0:
		elapsedMid.append(intervalStarts[i] -startingTime + interval/2)
		interval95th.append(p95)

assert len(elapsedMid) == len(interval95th)
fig,ax = plt.subplots()
fig.suptitle('95th percentile latency in interval for ' + trial)
ax.set_xlabel('elapsed time (ns)')
ax.set_ylabel('95th percentile latency')
ax.plot(elapsedMid,interval95th,'k-')
if saving:
	fig.savefig(trial+'/'+'interval_95th_ltc.jpg')
	plt.close(fig)
else:
	plt.show()





