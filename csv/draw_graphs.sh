#!/bin/sh

cp ./merge_csv.sh ./hpc_download/
cd ./hpc_download/
sh ./merge_csv.sh
cp ./merged_results.csv ../
rm ./merge_csv.sh
rm ./merged_results.csv
cd ..
sh preset_to_number.sh merged_results.csv out.csv
python3 graphs.py out.csv
