#!/usr/bin/python

import sys
import json

spark_log_file = sys.argv[1]
timestamp = 0
if "inprogress" in spark_log_file:
	timestamp = int(spark_log_file[-24:-11])
else:
	timestamp = int(spark_log_file[-13:])
#print timestamp
NOT_list = [] #number of tasks for event
subTime_list = [] #submisstion time for event
compTime_list = [] #Completion time for event
subDelay_list = [] #delay from timestamp for submission time of event
compDelay_list = [] #delay from timestamp for completion time of event

sparkLog = open(spark_log_file,'r')
with sparkLog:
	lines = sparkLog.readlines()
	for line in lines:
		event = json.loads(line)
		if 'Event' in event:
			if "stagecompleted" in event["Event"].lower(): 
#				print json.dumps(event, indent=2)
				print "Event : " + event["Event"]
				if 'Stage Info' in event:
					if 'Stage Name' in event["Stage Info"]:
						print "Stage Name: " + event["Stage Info"]["Stage Name"]
					if 'Number of Tasks' in event["Stage Info"]:
						print "Number of Tasks: " + str(event["Stage Info"]["Number of Tasks"])
						NOT_list.append(event["Stage Info"]["Number of Tasks"])
					if 'Submission Time' in event["Stage Info"]:
						print "Submission Time :" +str( event["Stage Info"]["Submission Time"]) + "; delay: " + str((event["Stage Info"]["Submission Time"] - timestamp)/1000.0)
						subTime_list.append(event["Stage Info"]["Submission Time"])
						subDelay_list.append(event["Stage Info"]["Submission Time"] - timestamp)
					if 'Completion Time' in event["Stage Info"]:
						print "Completion Time :" +str( event["Stage Info"]["Completion Time"]) + "; delay: " + str((event["Stage Info"]["Completion Time"] - timestamp)/1000.0)
						compTime_list.append(event["Stage Info"]["Completion Time"])
                                                compDelay_list.append(event["Stage Info"]["Completion Time"] - timestamp)
				print ""
		else:
			print json.dumps(event, indent=2)
			sparkLog.close()
			sys.exit("There is something in the log that does not have Event as an entry")
sparkLog.close()
if(len(NOT_list) != len(subTime_list) or len(NOT_list) != len(compTime_list)):
	print len(NOT_list)
	print len(subTime_list)
	print len(compTime_list)
	sys.exit("The lists are not of the same length")
#compute execution time and writes everything to file
i = 0
analysisFile = open(spark_log_file + "_analysis",'w')
for i in range(len(NOT_list)):
	analysisFile.write(str(subTime_list[i]))
	analysisFile.write(' ')
	analysisFile.write(str(compTime_list[i]))
	analysisFile.write(' ')
	analysisFile.write(str(subDelay_list[i]))
	analysisFile.write(' ')
	analysisFile.write(str(compDelay_list[i]))
	analysisFile.write(' ')
	analysisFile.write(str(NOT_list[i]))
        analysisFile.write(' ')
	analysisFile.write(str(compTime_list[i]-subTime_list[i]))
	analysisFile.write('\n')
analysisFile.close()

