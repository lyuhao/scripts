#!/usr/bin/python
import sys
import subprocess

if len(sys.argv) < 2:
	print "please provide qps level"
	exit(1)

qpsLevel = sys.argv[1]

for i in range (1,10):
	trial = 'q'+qpsLevel+'k'+str(i)
	csvPath = trial+'/'+trial+'.csv'
	print 'processing ' + csvPath
	subprocess.call(['./correct_csv.py', csvPath])
	subprocess.call(['./see_csv_agg.py', csvPath])
