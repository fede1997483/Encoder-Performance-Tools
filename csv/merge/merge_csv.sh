#!/bin/sh

# Output merged CSV file
output_csv="merged_results.csv"

# Find all CSV files in the current directory
csv_files=`ls *.csv 2> /dev/null`

# Check if there are any CSV files to merge
if [ -z "$csv_files" ]; then
  echo "No CSV files found in the current directory to merge."
  exit 1
fi

# Get the first CSV file to copy the header
first_file=`echo "$csv_files" | head -n 1`
head -n 1 "$first_file" > "$output_csv"

# Append data from each CSV file, excluding the header
for csv_file in $csv_files; do
  # Exclude the header line for all but the first file
  tail -n +2 "$csv_file" >> "$output_csv"
done

echo "Merged CSV file created: $output_csv"
