#!/usr/bin/python
import matplotlib.pyplot as plt

class BinAnalysis:

	

	

	def __init__(self):

		self.BIN_TYPE_TO_COLUMN_NUMBER = {
		'id' : 0,
		'generation_time' : 1,
		'queue_time' : 2,
		'service_time' : 3,
		'latency' : 4,
		'service_start_time' : 5,
		'instr_retired' : 6,
		'socket_read' : 7,
		'socket_write' : 8,
		'L3_miss_number' : 9,
		'L3_hit_rate' : 10,
		'time_on_server' : 11,
		'time_request_arrived_on_server' : 12,
		'worker_thread_core_id' : 13
		'L3_occupancy' : 14
	}
		self.BIN_COLUMN_NUMBER_TO_TYPE = {}
		self.bin_data = {}

		for type in self.BIN_TYPE_TO_COLUMN_NUMBER.keys():
			colmun_number = self.BIN_TYPE_TO_COLUMN_NUMBER[type]
			self.BIN_COLUMN_NUMBER_TO_TYPE[colmun_number] = type	

	def createNewKeyListPairInTableIfNotExist(self, key, table):
		if key not in table:
			table[key] = []

	def readBinFile(self, filePath):
		with open(filePath, 'r') as f:
			while True:
				line = f.readline()
				if line == "":
					break;
				datas = line.strip().split(' ')
				colmun_number = 0
				for data in datas:
					data_float_type = float(data)
					data_name = self.BIN_COLUMN_NUMBER_TO_TYPE[colmun_number]
					self.createNewKeyListPairInTableIfNotExist(data_name, self.bin_data)
					self.bin_data[data_name].append(data_float_type)
					colmun_number += 1

	def plotData(self, axis, xvar_name, yvar_name, line_style = 'k-', _label = ''):
		xvar_data = self.bin_data[xvar_name]
		yvar_data = self.bin_data[yvar_name]
		if _label == '':
			axis.plot(xvar_data, yvar_data, line_style)
		else:
			axis.plot(xvar_data, yvar_data, line_style, label = _label)

	def plotDataVsMemoryBandWidth(self, axis, yvar_name, line_style = 'k-', _label = ''):
		xvar_data = []
		for index, socket_read in enumerate(self.bin_data["socket_read"]):
    		soeckt_write = self.bin_data["socket_write"][idx]
    		memory_bandwidth = socket_read + socket_write
    		xvar_data.append(memory_bandwidth)
		yvar_data = self.bin_data[yvar_name]
		if _label == '':
			axis.plot(xvar_data, yvar_data, line_style)
		else:
			axis.plot(xvar_data, yvar_data, line_style, label = _label)

	def clearData(self):
		self.bin_data.clear()

	def getList(self,list_name):
		return self.bin_data[list_name]

