#!/usr/bin/python

import datetime
import pytz
from dateutil import parser
import math
from glob import glob

#useful constants
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

params = {}
NUMCORE=48

EPOCH = datetime.datetime.utcfromtimestamp(0)
LOCALTZONE = pytz.timezone ("America/Los_Angeles")

BUILTIN_COLORS = ['b', 'g', 'r', 'c', 'm', 'y', 'k'] #excluding 'w' (white) at the end

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
	params.clear()
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

# def getStartTime (line): #return nanoseconds
# 	line = line.strip()
# 	timeString = line[-28:]
# 	#print timeString
# 	naive = parser.parse(timeString)
# 	local_dt = LOCALTZONE.localize(naive, is_dst=True)
# 	utc_time = local_dt.astimezone(pytz.utc).replace(tzinfo=None)
# 	elapsed = (utc_time-EPOCH).total_seconds()
# 	# print elapsed
# 	return elapsed * 1e9

def getCsvTime (date, time):
	sTime = time.split('.')
	ms = float(sTime[1])
	time = sTime[0]
	dt = datetime.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S')
	local_dt = LOCALTZONE.localize(dt, is_dst=True)
	utc_time = local_dt.astimezone(pytz.utc).replace(tzinfo=None)
	elapsed = (utc_time-EPOCH).total_seconds()
	elapsed = (elapsed*1e3+ms)*1e6
	return elapsed

def get95th (aList):
	if len(aList) == 0:
		return -1
	if len(aList) == 1:
		return aList[0]
	sortedList = sorted(aList)
	percntileInterval = 100.0 /(float(len(sortedList)) - 1.0)
	indexFor95th = int(math.ceil(95.0 / percntileInterval))
	return sortedList[indexFor95th]

def getSparkTime(aFile): # returns system time when spark started in nanoseconds as float
	with open(aFile, 'r') as f:
		while True:
			line = f.readline()
			if line == '':
				sparkTime = -1
				break
			words = line.strip().split()
			if 'spark' not in words:
				continue
			sparkTime = float(words[-1])*1e9
			break
	return sparkTime

def pErr(aString, errNum=1): #short for print error
	print 'ERROR: ' + aString
	exit(int(errNum))

def pWarn(aString):
	print 'WARNING: ' + aString

def getDir(path): #ends with /
	tree = path.split('/')
	dirPath = ''
	for i in range(0, len(tree) - 1):
		dirPath = dirPath + tree[i] + '/'
	return dirPath

def getFileName(path):
	tree = path.split('/')
	return tree[-1]

def getRidOfLastFewCharacters(aString, length):
	return aString[:-length]

def parseWildCards(string) :
	return glob(string)

def getBuiltInColor(index):
	index = index % len(BUILTIN_COLORS)
	return BUILTIN_COLORS[index]

