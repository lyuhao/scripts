#!/usr/bin/python

import helpers
import sys
import matplotlib.pyplot as plt
import os.path
import OFFSET


save = False
if '-s' in sys.argv:
	save = True
	sys.argv.remove('-s')

trialFolder = str(sys.argv[1])
if not os.path.isdir(trialFolder):
	helpers.pErr('Folder' + trialFolder +' does not exist', 1)
qpsStr = trialFolder[1:-4] #trialFolder in format qxxx(x)fxxx

baseFolder = 'q'+qpsStr+'base'
if not os.path.isdir(baseFolder):
	helpers.pErr('Base folder ' + baseFolder + ' does not exist', 1)

timeFile = trialFolder +'/' + trialFolder+'.time'
if not os.path.isfile(timeFile):
	helpers.pErr('File ' + timeFile + ' does not exist' , 1)

#find spark starting time
sparkStartingTime = helpers.getSparkTime(timeFile)
if not sparkStartingTime > 0:
	helpers.pErr('Spark starting time not recorded in file ' + timeFile, 2)

#read through trial bin file and record
#dict to record ID : service time pair
#two dict: preSpark and postSpark
preSparkTime = {} #match id to list whose first elements is svcTime, second ltcTime
postSparkTime = {}

trialBin = trialFolder + '/' + trialFolder +'.bin'
print 'Reading from trial bin file'
with open (trialBin, 'r') as f:
	while True:
		line = f.readline()
		if line == '':
			break
		data = line.strip().split()
		rid = int(data[OFFSET.BIN['id']])
		rgen = int(data[OFFSET.BIN['generation']])
		rsvc = int(data[OFFSET.BIN['service']])
		rltc = int(data[OFFSET.BIN['latency']])
		times = [rsvc, rltc]
		if rgen >= sparkStartingTime:
			assert rid not in postSparkTime		
			postSparkTime[rid] = times
		else:
			assert rid not in preSparkTime
			preSparkTime[rid] = times

preSparkIds = []
preSparkTimeDiffs = [[], []] #two lists, first for service, second for latency
postSparkIds = []
postSparkTimeDiffs = [[] , []]

#read through base file
#get service time, calculate difference, append 
baseBin = baseFolder + '/' + baseFolder + '.bin'
print 'Reading from base bin file'
with open (baseBin,'r') as f:
	while True:
		line = f.readline()
		if line == '':
			break
		data = line.strip().split()
		rid = int(data[OFFSET.BIN['id']])
		rsvc = int(data[OFFSET.BIN['service']])
		rltc = int(data[OFFSET.BIN['latency']])

		if rid in preSparkTime:
			preSparkIds.append(rid)
			svcDiff = preSparkTime[rid][0] - rsvc
			ltcDiff = preSparkTime[rid][1] - rltc
			preSparkTimeDiffs[0].append(svcDiff)
			preSparkTimeDiffs[1].append(ltcDiff)
			del preSparkTime[rid]
		elif rid in postSparkTime:
			postSparkIds.append(rid)
			svcDiff = postSparkTime[rid][0] - rsvc
			ltcDiff = postSparkTime[rid][1] - rltc
			postSparkTimeDiffs[0].append(svcDiff)
			postSparkTimeDiffs[1].append(ltcDiff)
			del postSparkTime[rid]

		if len(preSparkTime) == 0 and len(postSparkTime) == 0:
			break

print 'Plotting'

fig = plt.figure()
fig.suptitle('Time difference against base', fontsize=16)
ax1 = plt.subplot('211')
ax1.set_title('Before sprak started',fontsize=12)
plt.plot(preSparkIds,preSparkTimeDiffs[0],'b.',label='svcDiff')
# plt.plot(preSparkIds,preSparkTimeDiffs[1],'bx',label='ltcDiff')
ax1.set_xlabel('request id', fontsize=12)
ax1.set_ylabel('difference (ns)', fontsize=12)
ax1.get_legend()
plt.axhline(y=0,color='k',linestyle='-')

ax2 = plt.subplot('212')
ax2.set_title('After sprak started',fontsize=12)
ax2.plot(postSparkIds,postSparkTimeDiffs[0],'r.',label='svcDiff')
# ax2.plot(postSparkIds,postSparkTimeDiffs[1],'rx',label='ltcDiff')
ax2.set_xlabel('request id', fontsize=12)
ax2.set_ylabel('difference (ns)', fontsize=12)
ax2.get_legend()
plt.axhline(y=0,color='k',linestyle='-')

fig.subplots_adjust(hspace=.4)
if save:
	path = trialFolder + '/' +'diff.jpg'
	print 'Saving plot to ' + path
	fig.savefig(path, dpi=1200)
	plt.close(fig)
else:
	plt.show()
	plt.close(fig)







