#!/usr/bin/python

# A simple script that prints line numbers and lines
# that has service time greater than a threshold
# argument: filename [threshold]
import matplotlib.pyplot as plt
import sys
import OFFSET

threshold = 3000000
input_file = str(sys.argv[1])

print "Reading data from " + input_file

if len(sys.argv) > 2:
	threshold = int(sys,argv[2])

with  open(input_file, 'r') as file:
	lineNumber = 0
	while True:
		line = file.readline()
		if line == '':
			break;
		lineNumber += 1
		datas = line.strip().split(' ')
		svcTime = int(datas[OFFSET.BIN['service']])
		if svcTime > threshold:
			print 'On line ' + str(lineNumber)+ ': service time is ' + str(svcTime) 

