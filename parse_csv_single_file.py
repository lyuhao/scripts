#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import csv 


import numpy as np

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from scipy.interpolate import griddata

number_core = 48


def read_one_trace(filename):
	#core = 5
	#load = 1000
	#filename = input_path+"6cores/"+"kmeans_xapian_"+str(load)+".csv"

	csv_file = open(filename,'r')
	core_start_column = [0] * number_core
	core_start_column[0] = 26*3 + 6 - 1

	be_ll3_cache_access_number = list()
	be_ll3_cache_miss_number = list()
	be_ll3_cache_miss_rate = list()


	for i in range(1,48):
		core_start_column[i] = core_start_column[i-1] + 16


	L3Miss_displacment = 4
	L3Hit_displacement = 6

	ls_cores = [12,13]
	be_cores = range(12,20)+range(36,44)

	i = 0
	for Row in csv_file:
		row = Row.split(';')

		if i < 2:
			i = i + 1
			continue

		i = i + 1
		L3Miss_sum = 0
		L3Hit_sum = 0

		for be_core in be_cores:
			start_column = core_start_column[be_core]
			L3Miss_location = start_column+L3Miss_displacment
			L3Hit_location = start_column+L3Hit_displacement
			L3Miss = float(row[L3Miss_location])
			L3Hit = float(row[L3Hit_location])

			if(L3Hit == 1):
				L3Miss_modified = 0
				L3access = 0
			else:
				L3Miss_modified = L3Miss
				L3access = L3Miss / (1-L3Hit)

			L3Miss_sum += L3Miss_modified
			L3Hit_sum += L3access*L3Hit

		if (L3access == 0):
			be_L3Miss_rate = 1
		else:
			be_L3Miss_rate = L3Miss_sum / (L3Miss_sum + L3Hit_sum)

		be_ll3_cache_miss_number.append(L3Miss_sum)
		be_ll3_cache_access_number.append(L3Hit_sum+L3Miss_sum)
		be_ll3_cache_miss_rate.append(be_L3Miss_rate)

	return be_ll3_cache_miss_rate,be_ll3_cache_miss_number




if (len(sys.argv) < 2):
	print "should provide input file path"
	exit(1)

filename = sys.argv[1]

be_ll3_cache_miss_rate,be_ll3_cache_miss_number = read_one_trace(filename)

t = range(0,len(be_ll3_cache_miss_number))

plt.plot(t,be_ll3_cache_miss_number)
plt.savefig(filename+"_llc.jpg")