#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import csv 


#import plotly.plotly as py
#import plotly.graph_objs as go 
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


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

fig,ax = plt.subplots()

for load in load_level:


	#print "--------load----------------------"+ str(load)
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

		#print i
		if i < 2:
			i = i + 1
			continue

		i = i + 1
		L3Miss_sum = 0
		L3Hit_sum = 0
		for ls_core in ls_cores:
			start_column = core_start_column[ls_core]
			L3Miss_location = start_column+L3Miss_displacment
			L3Hit_location = start_column+L3Hit_displacement
			#print row[L3Miss_location]
			L3Miss = float(row[L3Miss_location])
			L3Hit = float(row[L3Hit_location])
			
			##exceptional case ignore it
			if(L3Hit == 1):
				L3Miss_modified = 0
				L3access = 0
			else:
				L3Miss_modified = L3Miss
				L3access = L3Miss / (1-L3Hit)

			L3Miss_sum += L3Miss_modified
			L3Hit_sum += L3access*L3Hit

		if (L3access == 0):
			ls_L3Miss_rate = 1
		else:
			ls_L3Miss_rate = L3Miss_sum / (L3Miss_sum + L3Hit_sum)
		ls_ll3_cache_miss_number.append(L3Miss_sum)
		ls_ll3_cache_access_number.append(L3Hit_sum+L3Miss_sum)
		ls_ll3_cache_miss_rate.append(ls_L3Miss_rate)

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
		datapoints.append((load,L3Miss_sum,ls_L3Miss_rate))
	
	length = len(ls_ll3_cache_miss_rate) 

	t = np.linspace(0,length,length)
	#print len(ls_ll3_cache_miss_rate)
	#print len(be_ll3_cache_miss_rate)

	if(load == 1000):
		plt.plot(t,be_ll3_cache_miss_rate,'b',label='rate')
		plt.plot(t,[a/max(be_ll3_cache_miss_number) for a in be_ll3_cache_miss_number],'r',label='number')
	

	#plt.plot(t,be_ll3_cache_miss_rate,'b')
	#plt.title(str(load))	
	#plt.savefig(filename+str(load)+'.jpg')

	#plt.plot(ls_ll3_cache_miss_rate,be_ll3_cache_miss_number,'o')
	#plt.title(str(load))	 
	


legend = ax.legend(loc='upper center', shadow=True)
plt.title("batch last level cache miss rate at different load level")
plt.savefig(file_path+"batch_miss.jpg")
plt.clf()


xlist = list()
value = list()

max_be = 0
for point in datapoints:
	xlist.append([point[0],point[1]])
	max_be = max(point[1],max_be)
	value.append(point[2])


dt = np.dtype('int,float')
#print xlist
xarr = np.array(xlist)

varr = np.array(value)





grid_x,grid_y = np.meshgrid(np.arange(100,1001,1),np.arange(0,max_be,0.5))

#print grid_x.shape
#print grid_y.shape
#print xarr.shape
#print varr.shape


grid_z0 = griddata(xarr, varr, (grid_x, grid_y), method='nearest')

grid_z1 = griddata(xarr, varr, (grid_x, grid_y), method='linear')

grid_z2 = griddata(xarr, varr, (grid_x, grid_y), method='cubic')


fig = plt.figure()
ax = fig.gca(projection='3d')

surf = ax.plot_surface(grid_x,grid_y,grid_z0)


#ax.set_zlim(-1.01, 1.01)
#ax.zaxis.set_major_locator(LinearLocator(10))
#ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

plt.savefig(file_path+'ls_be_load.jpg')

#plot figure








	