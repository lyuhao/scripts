#!/usr/bin/python

import matplotlib.pyplot as plt
import sys
import os.path
AGG_OFFSET = {
	'aIPCls' : 1,
	'sL3MISSls' : 2,
	'sL3MISSb' : 3,
	'sL3ACCb' : 4,
}

BIN_OFFSET = {
	'latency' : 4,
	'service' : 3
}

if len(sys.argv) < 4:
	print "plot_latency_against.py [qpsLevel XVar YVar]"
	exit(1)

qpsLevel = sys.argv[1]
xvar = sys.argv[2]
yvar = sys.argv[3]

if xvar not in AGG_OFFSET:
	print "Canno identify parameter " + xvar
	print "please use one of the following: aIPCls sL3MISSls sL3MISSb SL3ACCb"
	exit(1)

if yvar not in BIN_OFFSET:
	print "Canno identify parameter " + xvar
	print "please use one of the following: latency service"
	exit(1)

xvarList = []
yvarList = []
for nCores in range(1,10):
	trial = 'q' + qpsLevel + 'k' + str(nCores)
	if not os.path.isdir(trial):
		print "Folder " + trial + " does not exist"
		exit(1)
	print 'Reading data from trial ' + trial
	binPath = trial+'/'+trial+'.bin'
	aggPath = trial+'/'+trial+'.agg'

	if not os.path.isfile(binPath):
		print "Bin file " + binPath + " does not exist"
		exit(1)
	if not os.path.isfile(aggPath):
		print "Agg file " + aggPath + " does not exist, please run see_csv_agg.py on csv file first"
		exit(1)

	binFile = open(binPath,'r')
	aggFile = open(aggPath,'r')

	aggCurLine = ''
	firstReqGenTime = -1


	aggLines = aggFile.readlines()
	aggLineNum = 0
	print 'Matching ' + yvar + ' with ' + xvar
	while True:
		binLine = binFile.readline().strip()
		if binLine == '': #reached end of line
			break
		times = binLine.split()
		if firstReqGenTime < 0:
			firstReqGenTime = int(times[1])
		elapsedTime = int(times[1]) + int(times[4])/2 - firstReqGenTime
		assert elapsedTime > 0
		yvarData = float(times[BIN_OFFSET[yvar]])
		yvarList.append(yvarData)
		# latency = int(times[4])
		# ltcList.append(latency)
		# print 'At time ' + str(times[1]) +  ', ' + str(elapsedTime) + 'ns has elapsed'

		#search for data point that is closest (in time) to when latency is generated
		found = False
		while found == False:
			aggLine = aggLines[aggLineNum].strip().split()
			if aggLineNum == len(aggLines) - 1:
				aggNextLine = aggLine
			else:
				aggNextLine = aggLines[aggLineNum + 1].strip().split()
			xVarData = float(aggLine[AGG_OFFSET[xvar]])
			elapsedTime0 = float(aggLine[0])
			elapsedTime1 = float(aggNextLine[0])
			try:
				assert elapsedTime1 >= elapsedTime0
			except AssertionError:
				print "AssertionError detected for elapsedTime1 >= elapsedTime0"
				print "\t" + str(aggLine)
				print '\t' + str(aggNextLine) 
				exit(1)
			if abs(elapsedTime0 - elapsedTime) <= abs(elapsedTime1 -elapsedTime):
				# print '\t Matched to elapsed time ' + str(elapsedTime0) + 'with ' +xvar + ' being ' + str(xVarData)
				found = True
			else:
				aggLineNum += 1
		xvarList.append(xVarData)

	aggFile.close()
	binFile.close()

print "Plotting"
fig,ax = plt.subplots()
fig.suptitle(yvar+ ' vs ' + xvar)
ax.set_xlabel(xvar)
ax.set_ylabel(yvar + ' time (ns)')
ax.plot(xvarList, yvarList, 'kx' )
fig.savefig('q' + qpsLevel + '_' + yvar + '_vs_' + xvar + '.jpg')
plt.close(fig)



