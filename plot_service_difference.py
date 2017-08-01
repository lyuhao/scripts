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
qpsStr = trialFolder[1:-2] #trialFolder in format qxxx(x)kx

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
preSparkSvc = {}
postSparkSvc = {}
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
		if rgen >= sparkStartingTime:
			assert rid not in postSparkSvc
			postSparkSvc[rid] = rsvc
		else:
			assert rid not in preSparkSvc
			preSparkSvc[rid] = rsvc

preSparkIds = []
preSparkDiffs = []
postSparkIds = []
postSparkDiffs = []
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
		if rid in preSparkSvc:
			preSparkIds.append(rid)
			svcDiff = preSparkSvc[rid] - rsvc
			preSparkDiffs.append(svcDiff)
			del preSparkSvc[rid]
		elif rid in postSparkSvc:
			postSparkIds.append(rid)
			svcDiff = postSparkSvc[rid] - rsvc
			postSparkDiffs.append(svcDiff)
			del postSparkSvc[rid]
		if len(preSparkSvc) == 0 and len(postSparkSvc) == 0:
			break

print 'Plotting'
fig,ax = plt.subplots()
fig.suptitle('Service time difference against base')
ax.plot(preSparkIds,preSparkDiffs,'gx')
ax.plot(postSparkIds,postSparkIds,'rx')
ax.set_xlabel('request id')
ax.set_ylabel('difference (ns)')
if save:
	fig.savefig(trialFolder + '/' +'svc_diff.jpg')
	plt.close(fig)
else:
	plt.show()
	plt.close(fig)







