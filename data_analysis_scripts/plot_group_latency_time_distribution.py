#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import helpers
import BinAnalysis

bin_analysis = BinAnalysis.BinAnalysis()

fig,ax = plt.subplots()
data_file_number = 0
percentile = 1
x_limit = -1
exclude_percentage = 0

if '-h' in sys.argv:
	print '--percentile=percentile'
	print '--x_limit=xlimit'
	exit()

for argument in sys.argv:
	if '--percentile=' in argument:
		percentile = float((argument.strip().split('='))[1])
		print 'Plotting up to ' + str(percentile) + " percentile"
		sys.argv.remove(argument)

for argument in sys.argv:
	if '--x_limit=' in argument:
		x_limit = float((argument.strip().split('='))[1])
		print 'Plotting with x_limit set to ' + str(x_limit)
		sys.argv.remove(argument)

for argument in sys.argv:
	if '--exclude=' in argument:
		exclude_percentage = float((argument.strip().split('='))[1])
		print 'excluding the first ' + str(exclude_percentage*100)+"% data"
		sys.argv.remove(argument)

for input_file in sys.argv[1:]:
	bin_analysis.readBinFile(input_file)

	sorted_latency_array = np.sort(bin_analysis.getList('latency'))

	sorted_latency_list = list(sorted_latency_array)

	caring_data_from_id = int(len(sorted_latency_list) * exclude_percentage)
	sorted_latency_list = sorted_latency_list[caring_data_from_id:]


	yvals_array = np.arange(len(sorted_latency_list))/float(len(sorted_latency_list))
	yvals_list = list(yvals_array)
	file_name = input_file[len(helpers.getDir(input_file)):]

	plot_start_id = int(len(sorted_latency_list) * exclude_percentage)

	ax.plot(sorted_latency_list,yvals_list,helpers.getBuiltInColor(data_file_number),label=file_name)
	bin_analysis.clearData()
	data_file_number += 1


fig.suptitle('Percentile vs. Latency')
ax.set_xlabel('latency (ns)')
ax.set_ylabel('percentile')
if x_limit > 0:
	ax.set_xlim([0, x_limit])
ax.set_ylim([0 , percentile])
plt.legend()
#plt.show()
fig.savefig(helpers.getDir(input_file)+'latency_distribution.jpg', dpi=1200)
plt.close(fig)
