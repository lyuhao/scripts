#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import os


trials = [ str(sys.argv[1]) , str(sys.argv[2]) ]

for i in range(0, len(trials)):
	if trials[i].endswith('/'):
		trials[i] = trials[i][:-1]

for trial in trials:
	if not os.path.isdir(trial):
		print "ERROR: trial " + trial  + 'not found'
		exit(1)

dirName = trials[0] + '_vs_' + trials[1]
if not os.path.isdir(dirName):
	os.mkdir(dirName)

paths = []
for trial in trials:
	paths.append(trial + '/' + trial + '.bin_cdf') 

percentiles = []
svcTimes = []
ltcTimes = []

for path in paths:
	percentiles.append([])
	svcTimes.append([])
	ltcTimes.append([])
	print "Reading data from " + path
	with open(path) as f:
		lines = f.readlines()
		for line in lines:
			times = line.split(' ')
			percentile = float(times[0])
			svcTime = float(times[1])
			ltcTime = float(times[2])

			percentiles[-1].append(percentile)
			svcTimes[-1].append(svcTime) 
			ltcTimes[-1].append(ltcTime) 

print "plotting distribution comparison"
fig,ax = plt.subplots()
fig.suptitle('Percentile vs. Time')
lineStyle = ['-', ':']
for i in range(0,len(trials)):
	ax.plot(svcTimes[i] ,percentiles[i],'g'+lineStyle[i],label=trials[i]+'SVC')
	ax.plot(ltcTimes[i] ,percentiles[i],'r'+lineStyle[i],label=trials[i]+'LTC')
ax.set_xlabel('time (ms)')
ax.set_ylabel('percentile')
plt.legend()
#plt.show()
fig.savefig(dirName+'/percentile_comparison.jpg')
plt.close(fig)



# print "Creating service time comparison plot"
# color = ['r' ,'g']

# fig,ax = plt.subplots()
# fig.suptitle('Service Time Comparison Between ' + trials[0] + ' and ' + trials[1])
# lineStyle = ['-', ':']
# for i in range(0,len(trials)):
# 	ax.plot(elapsedTimes[i] ,svcTimes[i],color[i],label=trials[i])
# ax.set_xlabel('elapsed timme (ns)')
# ax.set_ylabel('service time (ms)')
# plt.legend()
# #plt.show()
# fig.savefig(dirName+'/svcTime_comparison.jpg')
# plt.close(fig)

# print "Creating latency time comparison plot"
# fig,ax = plt.subplots()
# fig.suptitle('Latency Time Comparison Between ' + trials[0] + ' and ' + trials[1])

# for i in range(0,len(trials)):
# 	ax.plot(elapsedTimes[i] ,ltcTimes[i],color[i],label=trials[i])
# ax.set_xlabel('elapsed timme (ns)')
# ax.set_ylabel('latency time (ms)')
# plt.legend()
# #plt.show()
# fig.savefig(dirName+'/ltcTime_comparison.jpg')
# plt.close(fig)













# print "Sorting"

# sorted_service_time = np.sort(svcTimes)
# sorted_latency_time = np.sort(ltcTimes)

# sorted_service_time_list = list(sorted_service_time)
# sorted_latency_time_list = list(sorted_latency_time)

# assert len(sorted_latency_time) == len(sorted_service_time)
# yvals = np.arange(len(sorted_service_time))/float(len(sorted_service_time))
# yvals_list = list(yvals)

# print "Writing to cdf file"
# cdf_file = open(input_file+"_cdf",'w')

# index_95_l = 0 
# index_99_l = 0
# index_95_s = 0
# index_99_s = 0

# for i in range(0,len(yvals_list)):
# 	cdf_file.write(str(yvals_list[i]) + ' ')
# 	cdf_file.write(str(sorted_service_time_list[i])+' ') 
# 	cdf_file.write(str(sorted_latency_time_list[i])+'\n') 
# 	if ((yvals_list[i]- 0.99) < 1e-4):
# 		index_99 = i
# 	if ((yvals_list[i]-0.95) < 1e-4):
# 		index_95 = i
# cdf_file.close()

# print '95th-percentile service time: ' + str(sorted_service_time_list[index_95])
# print '99th-percentile service time: ' + str(sorted_service_time_list[index_99])
# print '95th-percentile latency time: ' + str(sorted_latency_time_list[index_95])
# print '99th-percentile latency time: ' + str(sorted_latency_time_list[index_99])

# print "Writing to analysis file"
# analysis_file = open(input_file+"_analysis",'w')
# analysis_file.write('95service:' + str(sorted_service_time_list[index_95]) + '\n')
# analysis_file.write('99service:' + str(sorted_service_time_list[index_99]) + '\n')
# analysis_file.write('95latency:' + str(sorted_latency_time_list[index_95]) + '\n')
# analysis_file.write('99latency:' + str(sorted_latency_time_list[index_99]) + '\n')
# analysis_file.close()

# print "plotting distribution"
# fig,ax = plt.subplots()
# fig.suptitle('Percentile vs. Time')
# ax.plot(sorted_service_time,yvals_list,'g',label='service')
# ax.plot(sorted_latency_time,yvals_list,'r',label='latency')
# ax.set_xlabel('time (ms)')
# ax.set_ylabel('percentile')
# plt.legend()
# #plt.show()
# fig.savefig(input_file+'_distribution.jpg')
# plt.close(fig)
