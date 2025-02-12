import pandas as pd

# Path to the input CSV file
input_file = "merged_results.csv"
# Path to the output CSV file
output_file = "filtered_out.csv"

# Read the CSV file without altering data types
data = pd.read_csv(input_file, dtype=str)

# Filter out rows where 'codec' column contains 'libvvenc'
filtered_data = data[data['codec'] != 'libvvenc']

# Save the filtered data to a new CSV file, preserving formatting
filtered_data.to_csv(output_file, index=False, quoting=1)

print(f"Filtered CSV file saved to {output_file}")
