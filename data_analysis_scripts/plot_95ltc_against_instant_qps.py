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
	intervalLtcs = [ [] for _ in xrange(len(intervalStarts)) ]

	for line in lines:
		datas = line.strip().split()
		reqGenTime = float(datas[1])
		reqLtcTime = float(datas[4])
		reqFinTime = reqGenTime + reqLtcTime
		eGenTime = reqGenTime - startingTime
		eFinTime = reqFinTime - startingTime
		numReqIntervalIndex = int(eGenTime / interval)
		intervalReqs[numReqIntervalIndex] += 1
		ltcIntervalIndex = int(eFinTime / interval)
		intervalLtcs[ltcIntervalIndex].append(reqLtcTime)


elapsedMid0 = [ s - startingTime + interval/2 for s in intervalStarts]
intervalQPSs = [ r * 1e9 / interval for r in intervalReqs]
assert len(elapsedMid0) == len(intervalQPSs)


elapsedMid1 = []
interval95th = []
for i in range(0,len(intervalStarts)):
	p95 = helpers.get95th(intervalLtcs[i])
	if p95 > 0:
		elapsedMid1.append(intervalStarts[i] -startingTime + interval/2)
		interval95th.append(p95)
assert len(elapsedMid1) == len(interval95th)
xlimit = [0, 5e9]

fig,ax1 = plt.subplots()
fig.suptitle('Comparison for instant qps and 95th percentile latency ' + trial)

ax1.set_xlabel('elapsed time (ns)')
ax1.set_ylabel('QPS', color='g')
ax1.plot(elapsedMid0,intervalQPSs,'gx')
ax1.tick_params('y',colors='g')
ax1.set_xlim(xlimit)

ax2=ax1.twinx()
ax2.set_ylabel('95th percentile latency')
ax2.plot(elapsedMid1,interval95th,'bx')
ax2.tick_params('y', colors='b')
ax2.set_xlim(xlimit)
# ax2.set_ylim([0, 8e6])

if saving:
	fig.savefig(trial+'/'+'iQPS_with_95ltc.jpg')
	plt.close(fig)
else:
	plt.show()
plt.close(fig)

fig,ax = plt.subplots()
fig.suptitle('95th Percentile Latency vs. Instant QPS')
ax.set_xlabel('instant QPS')
ax.set_ylabel('95th percentile')
ax.plot(intervalQPSs,interval95th,'kx')
if saving:
	fig.savefig(trial+'/'+'95ltc_vs_iQPS.jpg')
	plt.close(fig)
else:
	plt.show()
plt.close(fig)
