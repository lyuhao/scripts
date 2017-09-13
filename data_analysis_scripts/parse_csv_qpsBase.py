#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import csv 

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from scipy.interpolate import griddata

import os.path

#useful globals

params = {}
NUMCORE=48
CDISP = {   #dictionary for stats displacement for core
	'EXEC' : 0,
	'IPC' : 1,
	'FREQ' : 2,
	'AFREQ' : 3,
	'L3MISS' : 4,
	'L2MISS' : 5,
	'L3HIT' : 6,
	'L2HIT' : 7,
	'L3CLK' : 8,
	'L2CLK' : 9,
	'C0res' : 10,
	'C1res' : 11,
	'C3res' : 12,
	'C6res' : 13,
	'C7res' : 14,
	'TEMP' : 15
}
COL_PER_CORE=16



lineStyle = ['-', '--', '-.', ':']
lineColor = ['b', 'g', 'r', 'c', 'm', 'y', 'b']

#helper functions
def getColNum (letters): #take csv column index as input, output corresponding number to use
	sum = 0
	for letter in letters:
		sum *= 26
		numerical = ord(letter) - 64
		if numerical < 1  or numerical > 26:
			return -1
		else:
			sum += numerical
	return sum - 1

def readSetup (filePath):
	with open(filePath, 'r') as setup:
		for line in setup:
			line = line.strip()
			param = line.split("=")
			params[param[0]] = param[1]

def getCores (corestr):
	cores = list()
	corestr = corestr.strip()
	groups = corestr.split(",")
	for group in groups:
		bounds = group.split("-")
		if len(bounds) == 1:
			cores.append(int(bounds[0]))
		elif len(bounds) == 2:
			for c in range(int(bounds[0]),int(bounds[1])+1):
				cores.append(c)
		else:
			print ('getCores: parsing error')
			exit(1)
	return cores
			
def getL3Miss (row, cores):	#given cores ,and row, return L3Miss%, L3Miss#, and L3Access# as dict
	L3Miss_sum = 0
	L3Access_sum = 0
	
	for core in cores:
		try:
			L3MissN = float(row[ core_start_column[core] + CDISP['L3MISS'] ])
			L3MissP = 1 - float(row[ core_start_column[core] + CDISP['L3HIT'] ])
		except IndexError:
			print row
			print core
			print core_start_column[core] + CDISP['L3MISS']
			exit(1)

		if L3MissN == 0 or L3MissP == 0:
			print "WARNING: L3Miss number or percentage is 0 on row"
			print "\t" + row
			print "for core " + ls_core + ", data ignored"
			continue
		else:
			L3Access = L3MissN / L3MissP
		
		L3Miss_sum += L3MissN
		L3Access_sum += L3Access

	assert L3Access_sum > 0
	L3Miss_rate = L3Miss_sum / L3Access_sum
	result = {
		'L3MissN' : L3Miss_sum,
		'L3MissP' : L3Miss_rate,
		'L3AccessN' : L3Access_sum
	}
	return result

core_start_column = [0] * NUMCORE
core_start_column[0] = getColNum("CF")
for i in range(1,NUMCORE):
	core_start_column[i] = core_start_column[i-1] + COL_PER_CORE


##Start Execution

if (len(sys.argv) < 2):
	print "please provide desired QPS level"
	exit(1)
loadLevel = str(sys.argv[1])

for sparkNumCore in range(1,10):
	dirPath = "core" + str(sparkNumCore)
	if not os.path.isdir(dirPath):
		print "directory " + dirPath + " does not exist"
		exit(1)
	readSetup(dirPath + "/setup.txt")
	ls_cores = getCores(params["SERVERCORES"])

	IPC = {}

	for core in ls_cores:
		IPC[core] = []

	fileName = dirPath+"/kmeans_"+str(loadLevel)+".csv"
	if not os.path.isfile(fileName):
		print "ERROR: File " + fileName + " does not exist, exiting"
		exit(1)
	print "Processing " + fileName
	
	lineN = 0
	warmupLines = 2
	with open(fileName, 'rb') as csvfile:
		dataReader = csv.reader(csvfile, delimiter=';')
		for row in dataReader:
			lineN +=1

			if lineN <= warmupLines: #ignore the first two rows
				continue

			for core in ls_cores:
				coreIPC = float(row[ core_start_column[core] + CDISP['IPC'] ])
				IPC[core].append(coreIPC)
	#print data
	lineN -= warmupLines
	t = range(0, lineN)
	print sparkNumCore
	line_style = int(sparkNumCore)/len(lineColor)
	line_color = int(sparkNumCore)%len(lineColor)
	line_format = lineStyle[line_style] + lineColor[line_color]
	print line_format
	for core in ls_cores:
		plt.plot(t, IPC[core], line_format)

plt.show()


