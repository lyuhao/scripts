#!/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
import sys

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
	
	# curLine = 0

	# for curIntervalStart in np.arange(startingTime,endingTime,interval):
	# 	numReq = 0
	# 	print "current interval starting time: " + str(curIntervalStart)
	# 	while True:
	# 		datas = lines[curLine].strip().split()
	# 		reqGenTime = float(datas[1])
	# 		print "\tcurrent request generated at " + str(reqGenTime)
	# 		if reqGenTime < curIntervalStart:
	# 			eTimes.append(curIntervalStart + interval/2 - startingTime)
	# 			qpss.append(0)
	# 			print "\tcurrent interval contains no request"
	# 			break
	# 		if reqGenTime >=curIntervalStart + interval or curLine == len(lines) - 1:
	# 			qpsInInterval = numReq * 1e9 / interval
	# 			eTimes.append(curIntervalStart + interval/2 - startingTime)
	# 			qpss.append(qpsInInterval)
	# 			print '\tcurrent interval contains ' + str(numReq) + 'request, qps is ' + str(qpsInInterval)
	# 			break
	# 		else:
	# 			numReq+=1
	# 			curLine+=1
	# 			print 'Adding to interval, numReq in interval is now ' + str(numReq)
	elapsedMid = [ s - startingTime + interval/2 for s in intervalStarts]
	intervalQPSs = [ r * 1e9 / interval for r in intervalReqs]
	assert len(elapsedMid) == len(intervalQPSs)
fig,ax = plt.subplots()
fig.suptitle('Instant QPS for ' + trial)
ax.set_xlabel('elapsed time (ns)')
ax.set_ylabel('QPS')
ax.plot(elapsedMid,intervalQPSs,'k-')
fig.savefig(trial+'/'+'instant_qps.jpg')
plt.close(fig)




