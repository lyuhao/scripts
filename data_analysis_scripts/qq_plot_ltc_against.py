#!/usr/bin/python

import matplotlib.pyplot as plt
import sys
import os.path
AGG_OFFSET = {
	'aIPCls' : 1,
	'sL3MISSls' : 2,
	'sL3MISSb' : 3,
	'SL3ACCb' : 4,
}

if len(sys.argv) < 3:
	print "Usage: qq_plot.py [FOLDER XVar]"
	exit(1)

trial = sys.argv[1]
xvar = sys.argv[2]

if not os.path.isdir(trial):
	print "Folder " + trial + " does not exist"
	exit(1)

if xvar not in AGG_OFFSET:
	print "Canno identify parameter " + xvar
	print "please use one of the following: aIPCls sL3MISSls sL3MISSb SL3ACCb"
	exit(1)

binPath = trial+'/'+trial+'.bin'
aggPath = trial+'/'+trial+'.agg'

if not os.path.isfile(binPath):
	print "Bin file " + binPath + " does not exist"
	exit(1)
if not os.path.isfile(aggPath):
	print "Agg file " + aggPath + " does not exist, please run get_aggregate_data_from_csv.py on csv file first"
	exit(1)

binFile = open(binPath,'r')
aggFile = open(aggPath,'r')

aggCurLine = ''
firstReqGenTime = -1
xvarList = []
ltcList = []
xvar_to_ltc = {}

aggLines = aggFile.readlines()
aggLineNum = 0
print 'Matching latency with ' + xvar
while True:
	binLine = binFile.readline().strip()
	if binLine == '': #reached end of line
		break
	times = binLine.split()
	if firstReqGenTime < 0:
		firstReqGenTime = int(times[1])
	elapsedTime = int(times[1]) + int(times[4])/2 - firstReqGenTime
	assert elapsedTime > 0
	latency = int(times[4])
	if latency not in ltcList:
		ltcList.append(latency)
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
		if xVarData not in xvarList:
			xvarList.append(xVarData)
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

	if xVarData not in xvar_to_ltc:
		xvar_to_ltc[xVarData] = []
	xvar_to_ltc[xVarData].append(latency)

aggFile.close()
binFile.close()

# print xvarList
# print ltcList

#sort ltcList and xvarList
print 'Sorting...'
xvarList.sort()
ltcList.sort()

print "Converting to percentile "
xvarInterval = float(1) / float(( len(xvarList) - 1))
# print 'xvarInterval is ' + str(xvarInterval)
ltcInterval = float(1) / float(( len(ltcList) - 1))
# print 'ltcInterval is ' + str(ltcInterval)

xvarPercentileList = []
ltcPercentileList = []
for xvarValue in xvar_to_ltc:
	xvarPercentile = xvarList.index(xvarValue) * xvarInterval
	# print 'XvarValue ' + str(xvarValue) + 'was mapped to percentile ' + str(xvarPercentile)
	for ltcValue in xvar_to_ltc[xvarValue]:
		ltcPercentile = ltcList.index(ltcValue) * ltcInterval
		# print '\t Corresponding ltcValue ' + str(ltcValue) + 'was mapped to percentile ' + str(ltcPercentile)
 		xvarPercentileList.append(xvarPercentile)
		ltcPercentileList.append(ltcPercentile)

print "Plotting"
fig,ax = plt.subplots()
fig.suptitle('Latency vs ' + xvar + ': QQ plot')
ax.set_xlabel(xvar + '(perncetile)')
ax.set_ylabel('latency (percentile)')
ax.plot(xvarPercentileList, ltcPercentileList, 'kx' )
plt.show()



