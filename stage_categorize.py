#! /usr/bin/python
from sklearn.cluster import KMeans
import numpy
import sys
import fileinput
filePath = sys.argv[1]
content = open(filePath,'r')
kmeans_input_list = []
for line in content:
	data = line.split()
	kmeans_input_list.append([int(data[4]),int(data[5])])
content.close()
kmeans_input = numpy.array(kmeans_input_list)
kmeans = KMeans(n_clusters=int(sys.argv[2])).fit(kmeans_input)
print kmeans.labels_

