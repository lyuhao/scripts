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

	sorted_latency_array = np.sort(bin_analysis.getList('latency'))

	sorted_latency_list = list(sorted_latency_array)

	yvals_array = np.arange(len(sorted_latency_list))/float(len(sorted_latency_list))
	yvals_list = list(yvals_array)
	file_name = input_file[len(helpers.getDir(input_file)):]
	ax.plot(sorted_latency_list,yvals_list,helpers.getBuiltInColor(data_file_number),label=file_name)
	bin_analysis.clearData()
	data_file_number += 1


fig.suptitle('Percentile vs. Latency')
ax.set_xlabel('latency (ns)')
ax.set_ylabel('percentile')
ax.set_xlim([0, 1e8])
ax.set_ylim([0 ,0.99])
plt.legend()
#plt.show()
fig.savefig(helpers.getDir(input_file)+'latency_distribution.jpg', dpi=1200)
plt.close(fig)
