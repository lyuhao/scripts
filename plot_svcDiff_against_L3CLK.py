#!/usr/bin/python

import helpers
import sys
import matplotlib.pyplot as plt
import os.path
import OFFSET
import re
import subprocess

save = False
# parse if save figure or view
if '-s' in sys.argv:
	save = True
	sys.argv.remove('-s')

#confirm both trial and base folder exists
trialFolder = str(sys.argv[1])
if not os.path.isdir(trialFolder):
	helpers.pErr('Folder' + trialFolder +' does not exist', 1)
if 'q' in trialFolder:
	qpsStr = (re.split('q|k|f',trialFolder))[1]
baseFolder = 'q'+qpsStr+'base'
if not os.path.isdir(baseFolder):
	helpers.pErr('Base folder ' + baseFolder + ' does not exist', 1)

#get spark start time from time file in trial folder
timeFile = trialFolder +'/' + trialFolder+'.time'
if not os.path.isfile(timeFile):
	helpers.pErr('File ' + timeFile + ' does not exist' , 1)
#find spark starting time
sparkStartingTime = helpers.getSparkTime(timeFile)
if not sparkStartingTime > 0:
	helpers.pErr('Spark starting time not recorded in file ' + timeFile, 2)

#check to see if aggregate data exist, if not, run script to obtain it
scriptDir = helpers.getDir(sys.argv[0])
aggFile = trialFolder+'/'+trialFolder+'.agg'

if not os.path.isfile(aggFile):
	helpers.pWarn('No aggregate data file exists, running script to obtain from csv file')
	csvFile = trialFolder+'/'+trialFolder+'.csv'
	if not subprocess.call([scriptDir + 'get_aggregate_data_from_csv.py', csvFile]) == 0:
		helpers.pErr('Unable to get aggregate data from csv file')


print 'Reading all lines from aggregate data file'
aggFd = open(aggFile,'r')
aggLines = aggFd.readlines()
aggDatas = []
#pre-process for ease of using later
for aggline in aggLines:
	aggDatas.append(aggline.strip().split())
	aggLines.remove(aggline)




#read through trial bin file and record
#dict to record: ID, service time, corresponding L3CLK and L3MISS
#if server processing happens in one interval

#bascially I could calcualte end time based on service start time and service time
#if out of collection interval, ignore it


#two dict: preSpark and postSpark
preSparkTime = {} #match id to dict
postSparkTime = {}
firstReqGenTime = -1
trialBin = trialFolder + '/' + trialFolder +'.bin'
aggLineNum = 0 #always correspond to higher bound
interval_lower_bound = 0
interval_higher_bound = float(aggDatas[0][OFFSET.AGG['elapsed']])
print 'Reading from trial bin file and matching with aggregate data'
with open (trialBin, 'r') as f:
	
	while True:
		line = f.readline()
		if line == '': #EOF
			break
		data = line.strip().split()
		rid = int(data[OFFSET.BIN['id']])
		rgen = int(data[OFFSET.BIN['generation']])
		rsvc = int(data[OFFSET.BIN['service']])
		rltc = int(data[OFFSET.BIN['latency']])
		rsvcStart = int(data[OFFSET.BIN['svcStart']])
		if firstReqGenTime < 0:
			firstReqGenTime = rgen
		rsvcStartSinceFirstGen = rsvcStart - firstReqGenTime
		assert rsvcStartSinceFirstGen > 0
		rsvcFinishSinceFirstGen = rsvcStartSinceFirstGen + rsvc
		#find interval that contains start time
		#check if interval also contains end time
		#if not, ignore
		#if so, add data to corresponding dictionary
		# print 'Matching request ' + str(rid)
		# print rsvcStartSinceFirstGen
		# print interval_lower_bound
		while rsvcStartSinceFirstGen >= interval_higher_bound:
			aggLineNum = aggLineNum + 1
			interval_lower_bound = interval_higher_bound
			try:
				interval_higher_bound = float(aggDatas[aggLineNum][OFFSET.AGG['elapsed']])
			except IndexError:
				break
		while rsvcStartSinceFirstGen < interval_lower_bound:
			aggLineNum = aggLineNum - 1
			interval_higher_bound = interval_lower_bound
			if aggLineNum > 0:
				interval_lower_bound = float(aggDatas[aggLineNum - 1][OFFSET.AGG['elapsed']])
			else:
				interval_lower_bound = 0
		if rsvcFinishSinceFirstGen > interval_higher_bound :
			continue
		hiL3CLKls = float(aggDatas[aggLineNum][OFFSET.AGG['hiL3CLKls']])
		valueDict = {}
		valueDict['service'] = rsvc
		valueDict['hiL3CLKls'] = hiL3CLKls
		if rgen >= sparkStartingTime:
			assert rid not in postSparkTime		
			postSparkTime[rid] = valueDict
		else:
			assert rid not in preSparkTime
			preSparkTime[rid] = valueDict

preSparkIds = []
preSparkSvcDiffs = []
preSparkL3CLK = []

postSparkIds = []
postSparkSvcDiffs = []
postSparkL3CLK = []

#read through base file
#get service time, calculate difference, append 
#also append L3CLK 

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
		# rltc = int(data[OFFSET.BIN['latency']])

		if rid in preSparkTime:
			preSparkIds.append(rid)
			svcDiff = preSparkTime[rid]['service'] - rsvc
			hiL3CLKls = preSparkTime[rid]['hiL3CLKls']
			# ltcDiff = preSparkTime[rid][1] - rltc
			preSparkSvcDiffs.append(svcDiff)
			preSparkL3CLK.append(hiL3CLKls)
			# preSparkTimeDiffs[1].append(ltcDiff)
			del preSparkTime[rid]
		elif rid in postSparkTime:
			postSparkIds.append(rid)
			svcDiff = postSparkTime[rid]['service'] - rsvc
			# ltcDiff = postSparkTime[rid][1] - rltc
			hiL3CLKls = postSparkTime[rid]['hiL3CLKls']
			postSparkSvcDiffs.append(svcDiff)
			postSparkL3CLK.append(hiL3CLKls)
			del postSparkTime[rid]

		if len(preSparkTime) == 0 and len(postSparkTime) == 0:
			break

print 'Plotting'

fig = plt.figure()
fig.suptitle('Time difference against base', fontsize=16)
ax1 = plt.subplot('211')
ax1.set_title('Before sprak started',fontsize=12)
plt.plot(preSparkL3CLK,preSparkSvcDiffs,'b.',label='svcDiff')
# plt.plot(preSparkIds,preSparkTimeDiffs[1],'bx',label='ltcDiff')
ax1.set_xlabel('hiL3CLKls', fontsize=12)
ax1.set_ylabel('difference (ns)', fontsize=12)
ax1.get_legend()
plt.axhline(y=0,color='k',linestyle='-')

ax2 = plt.subplot('212')
ax2.set_title('After sprak started',fontsize=12)
ax2.plot(postSparkL3CLK,postSparkSvcDiffs,'r.',label='svcDiff')
# ax2.plot(postSparkIds,postSparkTimeDiffs[1],'rx',label='ltcDiff')
ax2.set_xlabel('hiL3CLKls', fontsize=12)
ax2.set_ylabel('difference (ns)', fontsize=12)
ax2.get_legend()
plt.axhline(y=0,color='k',linestyle='-')

fig.subplots_adjust(hspace=.4)
if save:
	path = trialFolder + '/' +'diff_against_L3CLK.jpg'
	print 'Saving plot to ' + path
	fig.savefig(path, dpi=1200)
	plt.close(fig)
else:
	plt.show()
	plt.close(fig)







