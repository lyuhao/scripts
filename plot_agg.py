#!/usr/bin/python

import matplotlib.pyplot as plt
import sys
import os.path
AGG_OFFSET = {
	'aIPCls' : 1,
	'sL3MISSls' : 2,
	'hiL3CLKls' : 3,
	'sL3MISSb' : 4,
	'sL3ACCb' : 5,
}

if len(sys.argv) < 5:
	print "plot_agg.py [group key XVar YVar]"
	exit(1)

group = sys.argv[1]
if group == 'trial':
	folders = [sys.argv[2]]
elif group == 'qps':
	qpsLevel = sys.argv[2]
	folders = ['q' + qpsLevel + 'k' + str(c) for c in range(1,10) ]
else:
	print "group " + group + ' cannot be understood'
	exit(1)

# print files
xvar = sys.argv[3]
yvar = sys.argv[4]

if xvar not in AGG_OFFSET:
	print "Canno identify parameter " + xvar
	print "please use one of the following: aIPCls sL3MISSls sL3MISSb sL3ACCb"
	exit(1)

if yvar not in AGG_OFFSET:
	print "Canno identify parameter " + yvar
	print "please use one of the following: aIPCls sL3MISSls sL3MISSb sL3ACCb"
	exit(1)

xvarList = []
yvarList = []
for folder in folders:
	if not os.path.isdir(folder):
		print "Folder " + folder + " does not exist"
		exit(1)
	print 'Reading data from folder ' + folder
	aggPath = folder+'/'+folder+'.agg'

	if not os.path.isfile(aggPath):
		print "Agg file " + aggPath + " does not exist, please run sget_aggregate_data_from_csv.py csv file first"
		exit(1)

	aggFile = open(aggPath,'r')

	print 'Reading ' + aggPath
	while True:
		aggLine = aggFile.readline().strip()
		if aggLine == '': #reached end of line
			break
		datas = aggLine.split()
		xvarData = float(datas[AGG_OFFSET[xvar]])
		xvarList.append(xvarData)
		yvarData = float(datas[AGG_OFFSET[yvar]])
		yvarList.append(yvarData)

	aggFile.close()

print "Plotting"
fig,ax = plt.subplots()
fig.suptitle(yvar+ ' vs ' + xvar)
ax.set_xlabel(xvar)
ax.set_ylabel(yvar)
ax.plot(xvarList, yvarList, 'kx' )
if group == 'trial':
	fig.savefig(sys.argv[2] +'/' + yvar + '_vs_' + xvar + '.jpg')
elif group == 'qps':
	fig.savefig('q' + sys.argv[2] + '_' + yvar + '_vs_' + xvar + '.jpg')
plt.close(fig)
