#!/bin/bash
echo "file x_varaible slope intercept r_value p_value std_err" > coefficients.txt
for file in ../server_characterization_data/xapian/*.bin; 
do
	echo "Processing $file"  
	./plot_service_time_vs_insn.py $file; 
	echo "$file insn $(cat regression.coefficient)" >> coefficients.txt; 
	./plot_service_time_vs_LLCO.py $file; 
	echo "$file LLCO $(cat regression.coefficient)" >> coefficients.txt; 
	./plot_service_time_vs_MBW.py $file; 
	echo "$file MBW $(cat regression.coefficient)" >> coefficients.txt; 
done

