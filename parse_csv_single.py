#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import csv 


#import plotly.plotly as py
#import plotly.graph_objs as go 
import numpy as np



from scipy.interpolate import griddata

import os.path

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


#parameters
if (len(sys.argv) < 2):
	print "should provide input file path"
	exit(1)

file_path = str(sys.argv[1])
if file_path.endswith('/'):
	file_path = file_path[:-1]
if not os.path.isdir(file_path):
	print "Please specify a valid file path"
	exit(1)

COL_PER_CORE=16

LS_CORES = [21,22,23]
BE_CORES = 12,36#range(14,24)+range(38,48)
number_core = 48
## statrdisplacement
L3Miss_displacment = 4
L3Hit_displacement = 6

load_level = range(100,200,100)

datapoints = list()

load_llc = dict()

for load in load_level:
	filename = file_path+"/kmeans_"+str(load)+".csv"
	core_start_column = [0] * number_core
	core_start_column[0] = getColNum("CV")
	for i in range(1,number_core):
		core_start_column[i] = core_start_column[i-1] + COL_PER_CORE

	be_ll3_cache_access_number = list()
	be_ll3_cache_miss_number = list()
	be_ll3_cache_miss_rate = list()

	ls_ll3_cache_access_number = list()
	ls_ll3_cache_miss_number = list()
	ls_ll3_cache_miss_rate = list()
	with open(filename, 'rb') as csvfile:
		dataReader = csv.reader(csvfile, delimiter=';')
		i = 0
		for row in dataReader:
			#print Row
			i = i + 1
			if i <= 2: #ignore the first two rows
				continue

			L3Miss_sum = 0
			L3Hit_sum = 0


			for ls_core in LS_CORES: #counting for server thread pool?
				start_column = core_start_column[ls_core]
				L3Miss_column = start_column+L3Miss_displacment
				L3Hit_column = start_column+L3Hit_displacement
				#print row[L3Miss_column]
				L3Miss = float(row[L3Miss_column])
				L3Hit = float(row[L3Hit_column])
				#L3access = L3Miss / (1-L3Hit) #clarify?
				L3Miss_sum += L3Miss
				L3Hit_sum += L3Hit

			L3Access = L3Miss_sum + L3Hit_sum
			ls_L3Miss_rate = L3Miss_sum / L3Access
			ls_ll3_cache_miss_number.append(L3Miss_sum)
			ls_ll3_cache_access_number.append(L3Access)
			ls_ll3_cache_miss_rate.append(ls_L3Miss_rate)

			L3Miss_sum = 0
			L3Hit_sum = 0

			for be_core in BE_CORES:
				start_column = core_start_column[be_core]
				L3Miss_colmun = start_column+L3Miss_displacment
				L3Hit_column = start_column+L3Hit_displacement
				L3Miss = float(row[L3Miss_colmun])
				L3Hit = float(row[L3Hit_column])
				#L3access = L3Miss / (1-L3Hit) #clarify?
				L3Miss_sum += L3Miss
				L3Hit_sum += L3Hit

			L3Access = L3Miss_sum + L3Hit_sum
			be_L3Miss_rate = L3Miss_sum / L3Access
			be_ll3_cache_miss_number.append(L3Miss_sum)
			be_ll3_cache_access_number.append(L3Access)
			be_ll3_cache_miss_rate.append(be_L3Miss_rate)
			
			datapoints.append((load,ls_ll3_cache_miss_rate,be_ll3_cache_miss_rate))
		
	length = len(ls_ll3_cache_miss_rate) 

	t = range(0, length)

	plt.plot(t,ls_ll3_cache_access_number,'r')
	plt.plot(t,be_ll3_cache_access_number,'b')
	plt.title(str(load))	
	plt.show()
	#plt.savefig(str(load)+'.jpg')




	