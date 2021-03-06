#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import csv 
input_file = sys.argv[1]
file = open(input_file)
service_time_list = list()
latency_time_list = list()
start_time_list = list()
with file:
	lines = file.readlines()
	for line in lines:
		times = line.split(' ')
		service_time = float(times[1])
		latency_time = float(times[0])+float(times[1])
		#start_time = float(times[2])
		service_time_list.append(service_time/1000000)
		latency_time_list.append(latency_time/1000000)
		#start_time_list.append(start_time/1000000)

##		print service_time/1000000,' ',latency_time/1000000 
	
sorted_service_time = np.sort(service_time_list)
sorted_latency_time = np.sort(latency_time_list)

sorted_service_time_list = list(sorted_service_time)
sorted_latency_time_list = list(sorted_latency_time)

#print list(sorted_service_time)
yvals_service = np.arange(len(sorted_service_time))/float(len(sorted_service_time))
#plt.plot(sorted_service_time,yvals_service)
#plt.show()

yvals_service_list = list(yvals_service)
file.close()

cdf_file = open(input_file+"_cdf",'w')

#for i in range(0,len(yvals_service_list)):
#	print str(sorted_service_time_list)+' '+str(yvals_service_list)+'\n'
#	cdf_file.write(str(sorted_service_time_list[i])+' '+str(yvals_service_list[i])+'\n') 

#convert start time to int

start_time_list = [int(st-start_time_list[0]) for st in start_time_list]

yvals_latency = np.arange(len(sorted_latency_time))/float(len(sorted_latency_time))
#plt.plot(sorted_latency_time,yvals_latency)
#plt.show()

yvals_latency_list = list(yvals_latency)

index_95 = 0 
index_99 = 0
index_50 = 0
index_75 = 0
for i in range(0,len(yvals_service_list)):
#	print str(sorted_service_time_list)+' '+str(yvals_service_list)+'\n'
	cdf_file.write(str(sorted_latency_time_list[i])+' '+str(yvals_latency_list[i])+'\n') 
	if ((yvals_latency_list[i]- 0.99) < 1e-4):
		index_99 = i
	if ((yvals_latency_list[i]-0.95) < 1e-4):
		index_95 = i
	if ((yvals_latency_list[i] - 0.5) < 1e-4):
		index_50 = i
	if ((yvals_latency_list[i] - 0.75) < 1e-4):
		index_75 = i

print 'median: ', sorted_latency_time_list[index_50]
print '75th-percentile: ', sorted_latency_time_list[index_75]
print '95th-percentile: ', sorted_latency_time_list[index_95]
print '99th-percentile: ', sorted_latency_time_list[index_99]


#start_time_list = range(0,len(service_time_list));
#plt.figure(1)
#plt.subplot(211)
#plt.plot(start_time_list,service_time_list,'b')
#plt.xlabel('GenTime')
#plt.ylabel('Service Time')
#plt.ylim([0,20])

#plt.subplot(212)
#plt.plot(start_time_list,latency_time_list,'r')
#plt.xlabel('GenTime')
#plt.ylabel('latency time')

#plt.show()