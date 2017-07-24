#!/usr/bin/python

import sys
import csv 

import os.path

import helpers

from tempfile import NamedTemporaryFile
import shutil


# corrects csv file produced by Intel Performance Monitor
# Specifically, add one second to time where it is smaller than previous row,
# and verify that the changed time is smaller than next row
def convertToTimeStr(num):
	assert num >=0 and num < 60
	if num < 10:
		retStr = '0' + str(newSecond)
	else:
		retStr = str(newSecond)
	return retStr


if len(sys.argv) < 2:
	print "please provide csv file"
	exit(1)

csvFile = str(sys.argv[1])
tempFile = NamedTemporaryFile(delete=False)
logFile = csvFile + '.correctionLog'
if not os.path.isfile(csvFile):
	print "Input csv file does not exist"
	exit(1)

lineN = 0
warmupLines = 2
dTimes = []
print "Attempting to correct CSV File"
log = open(logFile, 'w')

previousLineChanged = False
with open(csvFile, 'rb') as csvfile, tempFile:
	dataReader = csv.reader(csvfile, delimiter=';')
	writer = csv.writer(tempFile, delimiter=';')
	for row in dataReader:
		lineN +=1

		if lineN <= warmupLines:  #copy the first two lines exactly
			writer.writerow(row)
			continue

		dataTime = helpers.getCsvTime(row[0], row[1])
		if previousLineChanged:
			assert dataTime > dTimes[-1]
			previousLineChanged = False
		if len(dTimes) > 0:
			if dataTime <= dTimes[-1]:
				# print "Incorrect time detected for row " + str(lineN)
				originalTime = row[1]
				# print "original time is " + row[1] + ", corresponds to " + str(dataTime) + ' ns'
				#need to modify row
				digits = row[1].split(':')
				seconds = digits[2].split('.')
				newSecond = (int(seconds[0]) + 1) % 60
				if newSecond == '0':
					newMinute = (int(digits[1]) + 1) % 60
					newMinStr = convertToTimeStr(newMinute)
					digits[1] = newMinStr
					if newMinute == 0:
						newHour = (int(digits[0]) + 1) % 24
						newHourStr = convertToTimeStr(newHour)
						digits[0] = newHourStr
				newSecStr = convertToTimeStr(newSecond)
				row[1] = digits[0] + ':' + digits[1] + ':' +newSecStr + '.' + seconds[1]
				dataTimeCorrect = helpers.getCsvTime(row[0], row[1])
				assert dataTimeCorrect > dTimes[-1]
				# print "Changing to " + row[1] + ", corresponds to " + str(dataTimeCorrect) + ' ns'
				#put in correction log
				log.write('On line ' + str(lineN) + ':\n')
				log.write('\t changed time from ' + originalTime + ' to ' + row[1] +'\n')
				dataTime = dataTimeCorrect
				previousLineChanged = True
		dTimes.append(dataTime)
		writer.writerow(row)
log.close()
shutil.move(tempFile.name, csvFile)

