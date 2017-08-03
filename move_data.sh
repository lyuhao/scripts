#!/bin/bash

for QPS in {100..1000..100}
do
	if [ -d "q${QPS}base" ]
	then
		mv q${QPS}base/* turboOn/q${QPS}base/.
		rm -r q${QPS}base
	fi
	for core in {1..9..1}
	do
		if [ -d "q${QPS}k${core}" ]
		then
			mv q${QPS}k${core}/* turboOn/q${QPS}k${core}/.
			rm -r q${QPS}k${core}
		fi
	done
done
