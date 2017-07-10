#!/bin/bash


#parameter parsing
if [ "$#" -ne 2 ]
then
        echo "Please call the with the following format:"
        echo "./loop_run.sh [SERVER SPARKAPP]"
        exit 1
fi
#arguments
SERVER=$1
SPARKAPP=$2

#parameters
SERVERCORES=21-23
CLIENTCORES=9-11

SPARKCORES=12,36
DATAFOLDER="core1"
NUMTASKS=7500000

if [ -d ${DATAFOLDER} ]
then
	rm -r ${DATAFOLDER}
fi
mkdir ${DATAFOLDER}	
touch ${DATAFOLDER}/setup.txt
echo -e "SERVER=${SERVER}\nSPARKAPP=${SPARKAPP}\nSERVERCORES=${SERVERCORES}" | tee -a ${DATAFOLDER}/setup.txt
echo -e "CLIENTCORES=${CLIENTCORES}\nSPARKCORES=${SPARKCORES}\nDATAfOLDER=${DATAFOLDER}" | tee -a ${DATAFOLDER}/setup.txt
echo -e "NUMTASKS=${NUMTASKS}" | tee -a ${DATAFOLDER}/setup.txt

for QPS in {500..1000..100}
do
	source ./run.sh ${QPS} ${SERVERCORES} ${CLIENTCORES} ${SERVER} ${SPARKAPP}
	mv ${SPARKAPP}_${QPS}.csv ${DATAFOLDER}/.
	mv lats.bin ${DATAFOLDER}/${QPS}.bin
	sleep 10
done

