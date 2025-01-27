import pandas as pd

# Path to the input CSV file
input_file = "merged_results.csv"
# Path to the output CSV file
output_file = "filtered_out.csv"

# Read the CSV file
data = pd.read_csv(input_file)

# Filter out rows where 'codec' column contains 'libvvenc'
filtered_data = data[data['codec'] != 'libvvenc']

# Save the filtered data to a new CSV file
filtered_data.to_csv(output_file, index=False)

print(f"Filtered CSV file saved to {output_file}")
