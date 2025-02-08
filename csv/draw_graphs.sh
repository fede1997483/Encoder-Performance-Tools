#!/bin/sh

cp ./merge_csv.sh ./hpc_download/
cd ./hpc_download/
sh ./merge_csv.sh
cp ./merged_results.csv ../
rm ./merge_csv.sh
rm ./merged_results.csv
cd ..
sh preset_to_number.sh merged_results.csv out.csv
python3 graphs_preset.py out.csv
python3 graphs_user_time.py out.csv
python3 bitrate_efficiency.py out.csv
python3 bitrate_efficiency_UHD.py out.csv
python3 bitrate_efficiency_FHD.py out.csv