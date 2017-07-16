#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import csv 

from scipy.interpolate import griddata

import os.path



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

interestedTrace = ['EXEC', 'IPC', 'FREQ', 'AFREQ', 'L3MISS', 'L2MISS', 'L3HIT','L2HIT', 'L3CLK', 'L2CLK']

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
			

if len(sys.argv) < 2:
	print "please provide csv file"
	exit(1)

csvFile = str(sys.argv[1])
trialName = ''

if csvFile.endswith('.csv'):
	trialName = csvFile[:-4]
else:
	trialName = csvFile
	csvFile = csvFile + '.csv'
#print trialName

if not os.path.isfile(csvFile):
	print "Input csv file does not exist"
	exit(1)

setupFile = trialName + '.setup'

if not os.path.isfile(setupFile):
	print "Cannot find setup file for trial " + setupFile
	exit(1)

readSetup(setupFile)

ls_cores = getCores(params["SERVERCORES"])
#print ls_cores


core_start_column = [0] * NUMCORE
core_start_column[0] = getColNum("CF")

for i in range(1,NUMCORE):
	core_start_column[i] = core_start_column[i-1] + COL_PER_CORE

#print core_start_column

#initialize data dict
datas = {}
for core  in ls_cores:
	datas[core] = {}
	for trace in interestedTrace:
		datas[core][trace] = []

print 'Reading data from csv file'
lineN = 0
warmupLines = 2
with open(csvFile, 'rb') as csvfile:
	dataReader = csv.reader(csvfile, delimiter=';')
	for row in dataReader:
		lineN +=1

		if lineN <= warmupLines: #ignore the first two rows
			continue

		for core in ls_cores:
			for trace in interestedTrace:
				data = float(row[core_start_column[core] + CDISP[trace] ])
				datas[core][trace].append(data)

print 'Plotting'
lineN -= warmupLines
t = range(0, lineN)

for core in ls_cores:
	for trace in interestedTrace:
		plt.suptitle('Core' + str(core) + ' ' + trace)
		plt.plot(t, datas[core][trace])
		plt.savefig(trialName+ '_core' + str(core) + '_' + trace + '.jpg' )
		plt.close()