#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import csv 

#import plotly.plotly as py
#import plotly.graph_objs as go 

from scipy.interpolate import griddata

import os.path



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
		sum *= 10
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
			

if (len(sys.argv) < 2):
	print "should provide input directory path"
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

print ls_cores
print be_cores



# LS_CORES = [21,22,23]
# BE_CORES = 12,36#range(14,24)+range(38,48)

# ## stat displacement
# L3Miss_displacment = 4
# L3Hit_displacement = 6

# load_level = range(100,200,100)

# datapoints = list()

# load_llc = dict()

# for load in load_level:
# 	filename = file_path+"/kmeans_"+str(load)+".csv"
# 	core_start_column = [0] * number_core
# 	core_start_column[0] = getColNum("CV")
# 	for i in range(1,number_core):
# 		core_start_column[i] = core_start_column[i-1] + COL_PER_CORE

# 	be_ll3_cache_access_number = list()
# 	be_ll3_cache_miss_number = list()
# 	be_ll3_cache_miss_rate = list()

# 	ls_ll3_cache_access_number = list()
# 	ls_ll3_cache_miss_number = list()
# 	ls_ll3_cache_miss_rate = list()
# 	with open(filename, 'rb') as csvfile:
# 		dataReader = csv.reader(csvfile, delimiter=';')
# 		i = 0
# 		for row in dataReader:
# 			#print Row
# 			i = i + 1
# 			if i <= 2: #ignore the first two rows
# 				continue

# 			L3Miss_sum = 0
# 			L3Hit_sum = 0


# 			for ls_core in LS_CORES: #counting for server thread pool?
# 				start_column = core_start_column[ls_core]
# 				L3Miss_column = start_column+L3Miss_displacment
# 				L3Hit_column = start_column+L3Hit_displacement
# 				#print row[L3Miss_column]
# 				L3Miss = float(row[L3Miss_column])
# 				L3Hit = float(row[L3Hit_column])
# 				#L3access = L3Miss / (1-L3Hit) #clarify?
# 				L3Miss_sum += L3Miss
# 				L3Hit_sum += L3Hit

# 			L3Access = L3Miss_sum + L3Hit_sum
# 			ls_L3Miss_rate = L3Miss_sum / L3Access
# 			ls_ll3_cache_miss_number.append(L3Miss_sum)
# 			ls_ll3_cache_access_number.append(L3Access)
# 			ls_ll3_cache_miss_rate.append(ls_L3Miss_rate)

# 			L3Miss_sum = 0
# 			L3Hit_sum = 0

# 			for be_core in BE_CORES:
# 				start_column = core_start_column[be_core]
# 				L3Miss_colmun = start_column+L3Miss_displacment
# 				L3Hit_column = start_column+L3Hit_displacement
# 				L3Miss = float(row[L3Miss_colmun])
# 				L3Hit = float(row[L3Hit_column])
# 				#L3access = L3Miss / (1-L3Hit) #clarify?
# 				L3Miss_sum += L3Miss
# 				L3Hit_sum += L3Hit

# 			L3Access = L3Miss_sum + L3Hit_sum
# 			be_L3Miss_rate = L3Miss_sum / L3Access
# 			be_ll3_cache_miss_number.append(L3Miss_sum)
# 			be_ll3_cache_access_number.append(L3Access)
# 			be_ll3_cache_miss_rate.append(be_L3Miss_rate)
			
# 			datapoints.append((load,ls_ll3_cache_miss_rate,be_ll3_cache_miss_rate))
		
# 	length = len(ls_ll3_cache_miss_rate) 

# 	t = range(0, length)

# 	plt.plot(t,ls_ll3_cache_access_number,'r')
# 	plt.plot(t,be_ll3_cache_access_number,'b')
# 	plt.title(str(load))	
# 	plt.show()
# 	#plt.savefig(str(load)+'.jpg')




	