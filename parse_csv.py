#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import csv 

number_core = 48

if (sys.argc <2):
	print "should provide input file"
	exit(1)


be_l3_cache_access_number = list()
be_ll3_cache_miss_number = list()

ls_ll3_cache_access_number = list()
ls_ll3_cache_miss_number = list()

input_file = sys.argv[1]
file = open(input_file)

csv_file = csv.reader(csvfile,delimiter=' ',quotechar='|')

core_start_column = [0] * number_core

core_start_column[0] = 26*2 + 6 - 1


for i in range(1,48):
	core_start_column[i] = core_start_column[i-1] + 16


## statrdisplacement
L3Miss_displacment = 4
L3Hit_displacement = 6

ls_core = [12,13]
be_core = range(14,24)+range(38,48)


for row in spamreader:
	