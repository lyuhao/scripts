#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import helpers
import BinAnalysis

bin_analysis = BinAnalysis.BinAnalysis()

fig,ax = plt.subplots()
data_file_number = 0

for input_file in sys.argv[1:]:
	bin_analysis.readBinFile(input_file)

	sorted_service_time_array = np.sort(bin_analysis.getList('service_time'))

	sorted_service_time_list = list(sorted_service_time_array)

	yvals_array = np.arange(len(sorted_service_time_list))/float(len(sorted_service_time_list))
	yvals_list = list(yvals_array)
	file_name = input_file[len(helpers.getDir(input_file)):]
	ax.plot(sorted_service_time_list,yvals_list,helpers.getBuiltInColor(data_file_number),label=file_name)
	bin_analysis.clearData()
	data_file_number += 1


fig.suptitle('Percentile vs. Service Time')
ax.set_xlabel('service time (ns)')
ax.set_ylabel('percentile')
ax.set_xlim([0, 10e6])
plt.legend()
#plt.show()
fig.savefig(helpers.getDir(input_file)+'service_distribution.jpg', dpi=1200)
plt.close(fig)
