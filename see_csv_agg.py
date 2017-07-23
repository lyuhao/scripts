#!/usr/bin/python

import matplotlib.pyplot as plt
import sys
import csv 

import os.path

import helpers



#creates plot that shows aggregated Cpu parameters
#also creates file suitable for future comparison

if len(sys.argv) < 2:
	print "please provide csv file"
	exit(1)

csvFile = str(sys.argv[1])

if csvFile.endswith('.csv'):
	noSuffix = csvFile[:-4]
else:
	noSuffix = csvFile
	csvFile = csvFile + '.csv'

if not os.path.isfile(csvFile):
	print "Input csv file does not exist"
	exit(1)

setupFile = noSuffix + '.setup'

if not os.path.isfile(setupFile):
	print "Cannot find setup file " + setupFile
	exit(1)

helpers.readSetup(setupFile)

lsa_cores =  helpers.getCores(helpers.params['SERVERCORES'])
ba_cores = []
if 'SPARKCORES' in helpers.params:
	ba_cores = helpers.getCores(helpers.params['SPARKCORES'])

core_start_column = [0] * helpers.NUMCORE
core_start_column[0] = helpers.getColNum("CF")

for i in range(1,helpers.NUMCORE):
	core_start_column[i] = core_start_column[i-1] + helpers.COL_PER_CORE

eTime = [] #elapsed time since moses finished warm up 
aIPCls = [] #average IPC for lsa
sL3MISSls = [] #sum of L3MISS for lsa
if len(ba_cores) > 0:
	sL3MISSb = [] #sum of L3MISS for ba
	sL3ACCb = [] #sum of L3 Access for ba

with open(noSuffix+'.bin', 'r') as f:
	lines = f.readlines()
	firstRequestGenTime = float((lines[0].split())[1])
	lastRequestFinTime = float((lines[-1].split())[1]) + float((lines[-1].split())[4])
print 'first request generated at' + str(firstRequestGenTime)
print 'last request finished at ' + str(lastRequestFinTime)

dataRaw = {}
for core in lsa_cores:
	dataRaw[core] = {}
	dataRaw[core]['IPC'] = []
	dataRaw[core]['L3MISS'] = []
for core in ba_cores:
	dataRaw[core] = {}
	dataRaw[core]['L3MISS'] = []
	dataRaw[core]['L3ACC'] = []

print 'Reading data from csv file'
lineN = 0
warmupLines = 2
with open(csvFile, 'rb') as csvfile:
	dataReader = csv.reader(csvfile, delimiter=';')
	for row in dataReader:
		lineN +=1

		if lineN <= warmupLines: #ignore the first two rows
			continue

		dataTime = helpers.getCsvTime(row[0], row[1])
		# print dataTime
		if dataTime < firstRequestGenTime:
			continue
		if dataTime > lastRequestFinTime:
			break
		elapsedTime = dataTime - firstRequestGenTime
		if len(eTime) > 0:
			try:
				assert elapsedTime > eTime[-1]
			except AssertionError:
				print "Assertion Error: elapsed time is smaller than previous elapsed time"
				print '\t' + str(row)
				print 'is translated to ' + str(elapsedTime) +', where as prvious one is ' + str(eTime[-1])
				exit(1)
		eTime.append(elapsedTime)
		for core in lsa_cores:
			cIPC = float(row[core_start_column[core] + helpers.CDISP['IPC'] ])
			cL3MISS = float(row[core_start_column[core] + helpers.CDISP['L3MISS'] ])
			dataRaw[core]['IPC'].append(cIPC)
			dataRaw[core]['L3MISS'].append(cL3MISS)
		for core in ba_cores:
			cL3MISS = float(row[core_start_column[core] + helpers.CDISP['L3MISS'] ])
			cL3HIT = float(row[core_start_column[core] + helpers.CDISP['L3HIT'] ])
			cL3ACC = cL3MISS/(1-cL3HIT)
			dataRaw[core]['L3MISS'].append(cL3MISS)
			dataRaw[core]['L3ACC'].append(cL3ACC)

#remove mega thread
for core in lsa_cores:
	average_core_IPC = sum(dataRaw[core]['IPC'])/len(dataRaw[core]['IPC'])
	if average_core_IPC < 1.0:
		lsa_cores.remove(core)
		del dataRaw[core]
		break

#compute aggregate data and also write to a file
print "Processing data and writing to file"
outFile = open(noSuffix + '.agg','w')
for i in range(0,len(eTime)):
	server_IPC_sum = 0
	server_L3MISS_sum = 0
	for core in lsa_cores:
		server_IPC_sum += dataRaw[core]['IPC'][i]
		server_L3MISS_sum += dataRaw[core]['L3MISS'][i]
	server_IPC_average = server_IPC_sum / len(lsa_cores)
	aIPCls.append(server_IPC_average)
	sL3MISSls.append(server_L3MISS_sum)

	batch_L3MISS_sum = 0
	batch_L3ACC_sum = 0
	for core in ba_cores:
		batch_L3MISS_sum += dataRaw[core]['L3MISS'][i]
		batch_L3ACC_sum += dataRaw[core]['L3ACC'][i]
	sL3MISSb.append(batch_L3MISS_sum)
	sL3ACCb.append(batch_L3ACC_sum)

	outFile.write(str(eTime[i]) + ' ' + str(server_IPC_average) + ' ' + str(server_L3MISS_sum) + ' ')
	outFile.write(str(batch_L3MISS_sum) + ' ' + str(batch_L3ACC_sum) + '\n')
outFile.close()


trialFolder = noSuffix.split('/')[0]

print 'Plotting'
plt.suptitle('Server Average IPC vs Time')
plt.plot(eTime, aIPCls)
plt.savefig(trialFolder + '/aIPC_vs_time.jpg' )
plt.close()

plt.suptitle('Server L3Miss sum vs Time')
plt.plot(eTime, sL3MISSls)
plt.savefig(trialFolder + '/L3Missls_vs_time.jpg' )
plt.close()

plt.suptitle('Batch L3Miss sum vs Time')
plt.plot(eTime, sL3MISSb)
plt.savefig(trialFolder + '/L3Missb_vs_time.jpg' )
plt.close()

plt.suptitle('Batch L3Access sum vs Time')
plt.plot(eTime, sL3ACCb)
plt.savefig(trialFolder + '/L3Accessb_vs_time.jpg' )
plt.close()