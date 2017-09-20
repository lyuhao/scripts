#!/usr/bin/python
import BinAnalysis
import matplotlib.pyplot as plt
import sys
import helpers

# plot service time vs. id on the same plot for 
# all files passed in as arguments

bin_analysis = BinAnalysis.BinAnalysis()

fig,ax = plt.subplots()
data_file_number = 0

for bin_file in sys.argv[1:]:
	bin_analysis.readBinFile(bin_file)
	line_color = helpers.getBuiltInColor(data_file_number)
	bin_analysis.plotData(ax, 'id', 'service_time', line_color + '.', bin_file)
	ax.set_xlabel('request id')
	ax.set_ylabel('service time (ns)')
	bin_analysis.clearData()
	data_file_number += 1

plt.legend()
#stored in the folder of the last processeed file
dir_path = helpers.getDir(bin_file)
save_pic_path =  dir_path + 'service_time_vs_id.jpg'
fig.savefig(save_pic_path, dpi=1200)
plt.close(fig)