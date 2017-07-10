#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import csv 


#import plotly.plotly as py
#import plotly.graph_objs as go 
import numpy as np



from scipy.interpolate import griddata

number_core = 48

if (len(sys.argv) < 2):
	print "should provide input file path"
	exit(1)



file_path = str(sys.argv[1])


load_level = range(100,1100,100)

filenames = [file_path+"kmeans_xapian_12,13_"+str(load) for load in load_level]




datapoints = list()

load_llc = dict()

for load in load_level:



	filename = file_path+"kmeans_xapian_"+str(load)+".csv"

	#csv_file = csv.reader(filename,delimiter=' ',quotechar='|')
	csv_file = open(filename,'r') 
	core_start_column = [0] * number_core
	core_start_column[0] = 26*3 + 6 - 1


	be_ll3_cache_access_number = list()
	be_ll3_cache_miss_number = list()
	be_ll3_cache_miss_rate = list()

	ls_ll3_cache_access_number = list()
	ls_ll3_cache_miss_number = list()
	ls_ll3_cache_miss_rate = list()

	for i in range(1,48):
		core_start_column[i] = core_start_column[i-1] + 16


	## statrdisplacement
	L3Miss_displacment = 4
	L3Hit_displacement = 6

	ls_cores = [12,13]
	be_cores = range(14,24)+range(38,48)

	i = 0
	for Row in csv_file:
		#print Row
		row = Row.split(';')

		if i < 2:
			continue

		i = i + 1
		L3Miss_sum = 0
		L3Hit_sum = 0
		for ls_core in ls_cores:
			start_column = core_start_column[ls_core]
			L3Miss_location = start_column+L3Miss_displacment
			L3Hit_location = start_column+L3Hit_displacement
			print row[L3Miss_location]
			L3Miss = int(row[L3Miss_location])
			L3Hit = int(row[L3Hit_location])
			L3access = L3Miss / (1-L3Hit)
			L3Miss_sum += L3Miss
			L3Hit_sum += L3Hit

		ls_L3Miss_rate = L3Miss_sum / (L3Miss_sum + L3Hit_sum)
		ls_ll3_cache_miss_number.append(L3Miss_sum)
		ls_ll3_cache_access_number.append(L3Hit_sum)
		ls_ll3_cache_miss_rate.append(ls_L3Miss_rate)

		L3Miss_sum = 0
		L3Hit_sum = 0

		for be_core in be_cores:
			start_column = core_start_column[be_core]
			L3Miss_location = start_column+L3Miss_displacment
			L3Hit_location = start_column+L3Hit_displacement
			L3Miss = int(row[L3Miss_location])
			L3Hit = int(row[L3Hit_location])
			L3access = L3Miss / (1-L3Hit)
			L3Miss_sum += L3Miss
			L3Hit_sum += L3Hit


		be_L3Miss_rate = L3Miss_sum / (L3Miss_sum + L3Hit_sum)
		be_ll3_cache_miss_number.append(L3Miss_sum)
		be_ll3_cache_access_number.append(L3Hit_sum)
		be_ll3_cache_miss_rate.append(be_L3Miss_rate)
		datapoints.append((load,ls_ll3_cache_miss_rate,be_ll3_cache_miss_rate))
	
	length = ls_ll3_cache_miss_rate 

	t = np.linspace(0,length,length*2)

	plt.plot(t,lls_ll3_cache_access_number,'r')
	plt.plot(t,be_ll3_cache_access_number,'b')
	plt.title(str(load))	
	plt.savefig(str(load)+'.jpg')


#xlist = list()
#value = list()

#for point in datapoints:
	#xlist.append(point[0],point[1])
	#value.append(point[2])

#xarr = np.array(xlist,dtype=dt)
#varr = np.value(value,dtype=dt)



#grid_x,grd_y = np.mgrid(np.arange(100,1001,1),np.arange(0,1,0.01))

#grid_z0 = griddata(xarr, varr, (grid_x, grid_y), method='nearest')

#grid_z1 = griddata(xarr, varr, (grid_x, grid_y), method='linear')

#grid_z2 = griddata(xarr, varr, (grid_x, grid_y), method='cubic')


#plot_surface(X,Y,Z)
#plot figure








	