#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import csv 

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from scipy.interpolate import griddata

import os.path

#useful globals

params = {}
NUMCORE=48
CDISP = {   #dictionary for stats displacement for core
	'EXEC' : 0,
	'IPC' : 1,
	'FREQ' : 2,
	'AFREQ' : 3,
	'L3MISS' : 4,
	'L2MISS' : 5,
	'L3HIT' : 6,
	'L2HIT' : 7,
	'L3CLK' : 8,
	'L2CLK' : 9,
	'C0res' : 10,
	'C1res' : 11,
	'C3res' : 12,
	'C6res' : 13,
	'C7res' : 14,
	'TEMP' : 15
}
COL_PER_CORE=16

#helper functions
def getColNum (letters): #take csv column index as input, output corresponding number to use
	sum = 0
	for letter in letters:
		sum *= 26
		numerical = ord(letter) - 64
		if numerical < 1  or numerical > 26:
			return -1
		else:
			sum += numerical
	return sum - 1

def readSetup (filePath):
	with open(filePath, 'r') as setup:
		for line in setup:
			line = line.strip()
			param = line.split("=")
			params[param[0]] = param[1]

def getCores (corestr):
	cores = list()
	corestr = corestr.strip()
	groups = corestr.split(",")
	for group in groups:
		bounds = group.split("-")
		if len(bounds) == 1:
			cores.append(int(bounds[0]))
		elif len(bounds) == 2:
			for c in range(int(bounds[0]),int(bounds[1])+1):
				cores.append(c)
		else:
			print ('getCores: parsing error')
			exit(1)
	return cores
			
def getL3Miss (row, cores):	#given cores ,and row, return L3Miss%, L3Miss#, and L3Access# as dict
	L3Miss_sum = 0
	L3Access_sum = 0
	
	for core in cores:
		try:
			L3MissN = float(row[ core_start_column[core] + CDISP['L3MISS'] ])
			L3MissP = 1 - float(row[ core_start_column[core] + CDISP['L3HIT'] ])
		except IndexError:
			print row
			print core
			print core_start_column[core] + CDISP['L3MISS']
			exit(1)

		if L3MissN == 0 or L3MissP == 0:
			print "WARNING: L3Miss number or percentage is 0 on row"
			print "\t" + row
			print "for core " + ls_core + ", data ignored"
			continue
		else:
			L3Access = L3MissN / L3MissP
		
		L3Miss_sum += L3MissN
		L3Access_sum += L3Access

	assert L3Access_sum > 0
	L3Miss_rate = L3Miss_sum / L3Access_sum
	result = {
		'L3MissN' : L3Miss_sum,
		'L3MissP' : L3Miss_rate,
		'L3AccessN' : L3Access_sum
	}
	return result



##Start Execution

if (len(sys.argv) < 2):
	print "please provide directory path"
	exit(1)

dirPath = str(sys.argv[1])

if dirPath.endswith('/'):
	dirPath = dirPath[:-1]
if not os.path.isdir(dirPath):
	print "Please specify a valid directory path"
	exit(1)

readSetup(dirPath + "/setup.txt")

ls_cores = getCores(params["SERVERCORES"])
be_cores = getCores(params["SPARKCORES"])
load_level = range(100,1100,100)



datapoints = {
	'load' : [],
	'be_l3_cache_miss_number': [],
	'ls_l3_cache_miss_rate' : []
}

core_start_column = [0] * NUMCORE
core_start_column[0] = getColNum("CF")

for i in range(1,NUMCORE):
	core_start_column[i] = core_start_column[i-1] + COL_PER_CORE



for load in load_level:
	fileName = dirPath+"/kmeans_"+str(load)+".csv"
	if not os.path.isfile(fileName):
		print "ERROR: File " + fileName + " does not exist, exiting"
		exit(1)
	print "Processing " + fileName
	be_ll3_cache_access_number = list()
	be_ll3_cache_miss_number = list()
	be_ll3_cache_miss_rate = list()

	ls_ll3_cache_access_number = list()
	ls_ll3_cache_miss_number = list()
	ls_ll3_cache_miss_rate = list()

	lineCount = 0
	startingLine = 3

	with open(fileName, 'rb') as csvfile:
		dataReader = csv.reader(csvfile, delimiter=';')
		for row in dataReader:
			lineCount +=1
			if lineCount < startingLine: #ignore the first two rows
				continue

			ls_l3 = getL3Miss(row, ls_cores)
			ls_ll3_cache_miss_number.append(ls_l3['L3MissN'])
			ls_ll3_cache_access_number.append(ls_l3['L3AccessN'])
			ls_ll3_cache_miss_rate.append(ls_l3['L3MissP'])

			be_l3 = getL3Miss(row, be_cores)
			be_ll3_cache_miss_number.append(be_l3['L3MissN'])
			be_ll3_cache_access_number.append(be_l3['L3AccessN'])
			be_ll3_cache_miss_rate.append(be_l3['L3MissP'])
	
	length = len(ls_ll3_cache_miss_rate) 

	loadList = [load] * length
	datapoints['load'] += loadList
	datapoints['be_l3_cache_miss_number'] += be_ll3_cache_miss_number
	datapoints['ls_l3_cache_miss_rate'] += ls_ll3_cache_miss_rate


	t = np.linspace(0,length,length)
	
	fig,ax1 = plt.subplots()
	fig.suptitle('Batch L3 Cache with Load = ' + str(load))
	ax1.plot(t,be_ll3_cache_miss_rate,'b',label='rate')
	ax1.set_xlabel('time (s)')
	ax1.set_ylabel('Miss Rate', color='b')
	ax1.tick_params('y',colors='b')

	ax2 = ax1.twinx()
	ax2.plot(t, be_ll3_cache_miss_number,'r',label='number')
	ax2.set_ylabel('Miss Number', color='r')
	ax2.tick_params('y',colors='r')
	
	fig.savefig(fileName[:-4] + "_batch_miss.jpg")
	fig.clf()
	plt.close(fig)

	fig,ax = plt.subplots()
	fig.suptitle('LS Miss Percentage vs. BE Miss Number with Load = ' + str(load))
	ax.plot(be_ll3_cache_miss_number,ls_ll3_cache_miss_rate,'o')
	ax.set_xlabel('Batch L3 Cache Miss Number')
	ax.set_ylabel('Moses L3 Cache Miss Rate')
	fig.savefig(fileName[:-4] + "_moses_vs_batch_miss.jpg")
	plt.close(fig)

print "Generating 3D Scatter Plot"
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(datapoints['load'],datapoints['be_l3_cache_miss_number'], datapoints['ls_l3_cache_miss_rate'])
ax.set_xlabel('Load')
ax.set_ylabel('Batch L3 Cache Miss Number')
ax.set_zlabel('Moses L3 Cache Miss Rate')
fig.savefig(dirPath + "/ls_be_load_scatter.jpg")
plt.close(fig)


print "Generating 3D Surface Plot"
xlist = []
value = datapoints['ls_l3_cache_miss_rate']
max_be = max(datapoints['be_l3_cache_miss_number'])

for index in range(0,len(datapoints['load'])):
	xlist.append( [ datapoints['load'][index] , datapoints['be_l3_cache_miss_number'][index] ] )

xarr = np.array(xlist)
varr = np.array(value)

grid_x,grid_y = np.meshgrid(np.arange(100,1001,1),np.arange(0,max_be,0.5))

grid_z0 = griddata(xarr, varr, (grid_x, grid_y), method='nearest')

grid_z1 = griddata(xarr, varr, (grid_x, grid_y), method='linear')

grid_z2 = griddata(xarr, varr, (grid_x, grid_y), method='cubic')


fig = plt.figure()
ax = fig.gca(projection='3d')

surf = ax.plot_surface(grid_x,grid_y,grid_z1)
ax.set_xlabel('Load')
ax.set_ylabel('Batch L3 Cache Miss Number')
ax.set_zlabel('Moses L3 Cache Miss Rate')

#ax.set_zlim(-1.01, 1.01)
#ax.zaxis.set_major_locator(LinearLocator(10))
#ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

plt.savefig(dirPath+'/ls_be_load_surface.jpg')

#plot figure








	