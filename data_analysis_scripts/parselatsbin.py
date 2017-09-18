#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys



input_file = str(sys.argv[1])
file = open(input_file)

ids = []
genTimes = []
svcTimes = []
ltcTimes = []
finTimes = []


print "Reading data from " + input_file

with file:
	lines = file.readlines()
	for line in lines:
		times = line.split(' ')
		rid = int(times[0])
		genTime = float(times[1])
		queueTime = int(times[2])
		svcTime = float(times[3])
		ltcTime = float(times[4])

		ids.append(rid)
		genTimes.append(genTime/1000000) #convert to ms
		svcTimes.append(svcTime/1000000) #convert to ms
		ltcTimes.append(ltcTime/1000000) #convert to ms
		finTimes.append((genTime+ltcTime)/1000000)
file.close()

print "Creating plots from raw data"

print "Creating latency and service  vs generation time plot"
fig,ax = plt.subplots()
fig.suptitle('Service and Response Time vs. Generation Time ')
ax.plot(genTimes,ltcTimes,'r-',label='latency')
ax.plot(genTimes, svcTimes,'g-',label='service')
ax.set_xlabel('generation time (ms)')
ax.set_ylabel('time (ms)')
plt.legend()
#plt.show()
fig.savefig(input_file+'_time_vs_gen.jpg')
plt.close(fig)

print "Sorting"

sorted_service_time = np.sort(svcTimes)
sorted_latency_time = np.sort(ltcTimes)

sorted_service_time_list = list(sorted_service_time)
sorted_latency_time_list = list(sorted_latency_time)

assert len(sorted_latency_time) == len(sorted_service_time)
yvals = np.arange(len(sorted_service_time))/float(len(sorted_service_time))
yvals_list = list(yvals)

print "Writing to cdf file"
cdf_file = open(input_file+"_cdf",'w')

index_95_l = 0 
index_99_l = 0
index_95_s = 0
index_99_s = 0

for i in range(0,len(yvals_list)):
	cdf_file.write(str(yvals_list[i]) + ' ')
	cdf_file.write(str(sorted_service_time_list[i])+' ') 
	cdf_file.write(str(sorted_latency_time_list[i])+'\n') 
	if ((yvals_list[i]- 0.99) < 1e-4):
		index_99 = i
	if ((yvals_list[i]-0.95) < 1e-4):
		index_95 = i
cdf_file.close()

print '95th-percentile service time: ' + str(sorted_service_time_list[index_95])
print '99th-percentile service time: ' + str(sorted_service_time_list[index_99])
print '95th-percentile latency time: ' + str(sorted_latency_time_list[index_95])
print '99th-percentile latency time: ' + str(sorted_latency_time_list[index_99])

print "Writing to analysis file"
analysis_file = open(input_file+"_analysis",'w')
analysis_file.write('95service:' + str(sorted_service_time_list[index_95]) + '\n')
analysis_file.write('99service:' + str(sorted_service_time_list[index_99]) + '\n')
analysis_file.write('95latency:' + str(sorted_latency_time_list[index_95]) + '\n')
analysis_file.write('99latency:' + str(sorted_latency_time_list[index_99]) + '\n')
analysis_file.close()

print "plotting distribution"
fig,ax = plt.subplots()
fig.suptitle('Percentile vs. Time')
ax.plot(sorted_service_time,yvals_list,'g',label='service')
ax.plot(sorted_latency_time,yvals_list,'r',label='latency')
ax.set_xlabel('time (ms)')
ax.set_ylabel('percentile')
plt.legend()
#plt.show()
fig.savefig(input_file+'_distribution.jpg')
plt.close(fig)
