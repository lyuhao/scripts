#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import csv 

import os.path

import helpers





interestedTrace = ['EXEC', 'IPC', 'FREQ', 'AFREQ', 'L3MISS', 'L2MISS', 'L3HIT','L2HIT', 'L3CLK', 'L2CLK']

if len(sys.argv) < 3:
	print "please call with the following format:"
	print "\t compareCsv.py trial1 trial2"
	exit(1)

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
	paths.append(trial + '/' + trial + '.csv') 


for path in paths:
	if not os.path.isfile(path):
		print "ERROR: csv file " + path + " does not exist"
		exit(1)

core_start_column = [0] * helpers.NUMCORE
core_start_column[0] = helpers.getColNum("CF")

for i in range(1,helpers.NUMCORE):
	core_start_column[i] = core_start_column[i-1] + helpers.COL_PER_CORE

datas = {}
trialCores=[]

for i in range(0,len(trials)):

	setupFile = trials[i] + '/' + trials[i] + '.setup'

	if not os.path.isfile(setupFile):
		print "Cannot find setup file for trial " + setupFile
		exit(1)

	helpers.readSetup(setupFile)

	ls_cores = helpers.getCores(helpers.params["SERVERCORES"])
	trialCores.append(ls_cores)
	with open(trials[i] + '/' + trials[i] + '.bin', 'r') as f:
		lines = f.readlines()
		firstRequestGenTime = float((lines[0].split())[1])
		lastRequestFinTime = float((lines[-1].split())[1]) + float((lines[-1].split())[4])
	mosesDuration = lastRequestFinTime - firstRequestGenTime
	assert mosesDuration > 0
	# print 'first request generated at' + str(firstRequestGenTime)
	# print 'last request generated at ' + str(lastRequestGenTime)

	datas[trials[i]] = {}
	datas[trials[i]]['elapsedTimes'] = []

	for core  in ls_cores:
		datas[trials[i]][core] = {}
		for trace in interestedTrace:
			datas[trials[i]][core][trace] = []

	print 'Reading data from ' + paths[i]
	lineN = 0
	warmupLines = 2
	with open(paths[i], 'rb') as csvfile:
		dataReader = csv.reader(csvfile, delimiter=';')
		for row in dataReader:
			lineN +=1

			if lineN <= warmupLines: #ignore the first two rows
				continue

			dataTime = helpers.getCsvTime(row[0], row[1])
			# print dataTime
			if dataTime < firstRequestGenTime:
				continue
			elapsedTime = dataTime - firstRequestGenTime
			if elapsedTime > mosesDuration:
				break
			datas[trials[i]]['elapsedTimes'].append(elapsedTime)
			for core in ls_cores:
				for trace in interestedTrace:
					data = float(row[core_start_column[core] + helpers.CDISP[trace] ])
					datas[trials[i]][core][trace].append(data)
# print trialCores
assert len(trialCores[0]) == len(trialCores[1])
print 'Plotting'
lineColor = ['r','g']
for trace in interestedTrace:
	for c in range(0,len(trialCores[0])):
			plt.subplots
			plt.suptitle(trace +': ' + trials[0] + 'Core' + str(trialCores[0][c]) + 'vs' + trials[1] + 'Core' + str(trialCores[1][c]))
			plt.plot(datas[trials[0]]['elapsedTimes'], datas[trials[0]][trialCores[0][c]][trace], 'r', label=trials[0])
			plt.plot(datas[trials[1]]['elapsedTimes'], datas[trials[1]][trialCores[0][c]][trace], 'g', label=trials[1])
			plt.xlabel('elapsed time (ns)')
			plt.legend()
			plt.savefig(dirName + '/' +trace +': ' + trials[0] + 'Core' + str(trialCores[0][c]) + 'vs' + trials[1] + 'Core' + str(trialCores[1][c]) + '.jpg' )
			plt.close()