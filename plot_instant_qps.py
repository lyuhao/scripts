#!/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
import sys

saving = False
if '-s' in sys.argv:
	saving = True
	sys.argv.remove('-s')

trial = sys.argv[1]
binPath = trial + '/' + trial + '.bin'
interval = 50e6 #50ms, converting to ns
eTimes = []
qpss = []



with open(binPath, 'r') as binFile:
	lines = binFile.readlines()
	startingTime = float(lines[0].strip().split()[1])
	endingTime = float(lines[-1].strip().split()[1]) + float(lines[-1].strip().split()[4])
	print 'Starting Time: ' + str(startingTime)
	print 'Ending Time: ' + str(endingTime)
	intervalStarts = np.arange(startingTime,endingTime,interval).tolist()
	intervalReqs = [0] * len(intervalStarts)
	for line in lines:
		datas = line.strip().split()
		reqGenTime = float(datas[1])
		elapsedTime = reqGenTime - startingTime
		intervalIndex = int(elapsedTime / interval)
		intervalReqs[intervalIndex] +=1

	elapsedMid = [ s - startingTime + interval/2 for s in intervalStarts]
	intervalQPSs = [ r * 1e9 / interval for r in intervalReqs]
	assert len(elapsedMid) == len(intervalQPSs)
fig,ax = plt.subplots()
fig.suptitle('Instant QPS for ' + trial)
ax.set_xlabel('elapsed time (ns)')
ax.set_ylabel('QPS')
ax.plot(elapsedMid,intervalQPSs,'k-')
if saving:
	fig.savefig(trial+'/'+'interval_95th_ltc.jpg')
	plt.close(fig)
else:
	plt.show()

