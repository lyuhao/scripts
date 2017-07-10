#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import csv 

import plotly.plotly as py
import plotly.graph_objs as go 
import numpy as np
number_core = 48

if (sys.argc <2):
	print "should provide input file"
	exit(1)


load_level = range(100,1100,100)

filenames = ["kmeans_xapian_12,13_"+str(load) for load in load_level]


be_l3_cache_access_number = list()
be_ll3_cache_miss_number = list()

ls_ll3_cache_access_number = list()
ls_ll3_cache_miss_number = list()

input_file = sys.argv[1]
file = open(input_file)


load_llc = dict()

for load in load_level:

	filename = "kmeans_xapian_12,13_"+str(load)
	csv_file = csv.reader(csvfile,delimiter=' ',quotechar='|')
	core_start_column = [0] * number_core
	core_start_column[0] = 26*2 + 6 - 1


	for i in range(1,48):
		core_start_column[i] = core_start_column[i-1] + 16


	## statrdisplacement
	L3Miss_displacment = 4
	L3Hit_displacement = 6

	ls_cores = [12,13]
	be_cores = range(14,24)+range(38,48)


	for row in csvfile:
		L3Miss_sum = 0
		L3Hit_sum = 0
		for ls_core in ls_cores:
			start_column = core_start_column[ls_core]
			L3Miss_displacment = start_column+4
			L3Hit_displacement = start_column+6
			L3Miss = row[L3Miss_displacment]
			L3Hit = row[L3Hit_displacement]
			L3access = L3Miss / (1-L3Hit)
			L3Miss_sum += L3Miss
			L3Hit_sum += L3Hit
		ls_ll3_cache_miss_number.append(L3Miss_sum)
		ls_ll3_cache_access_number.append(L3Hit_sum)

		L3Miss_sum = 0
		L3Hit_sum = 0

		for be_core in be_cores:
			start_column = core_start_column[be_core]
			L3Miss_displacment = start_column+4
			L3Hit_displacement = start_column+6
			L3Miss = row[L3Miss_displacment]
			L3Hit = row[L3Hit_displacement]
			L3access = L3Miss / (1-L3Hit)
			L3Miss_sum += L3Miss
			L3Hit_sum += L3Hit

		be_ll3_cache_miss_number.append(L3Miss_sum)
		be_ll3_cache_access_number.append(L3Hit_sum)

 	load_llc[load] = 

#plot figure








	