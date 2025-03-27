import pandas as pd
import numpy as np

file_path = "out.csv"
df = pd.read_csv(file_path)

fhd_df = df[df['seq_name'].str.contains("1080p|FHD", case=False, na=False)]

fhd_df['vmaf_bin'] = fhd_df['vmaf'].apply(lambda x: int(np.floor(x)))

hevc_df = fhd_df[(fhd_df['codec'] == 'libx265') & (fhd_df['preset'] == 2)]
hevc_min_bitrate = hevc_df.groupby(['seq_name', 'vmaf_bin'])['actual_bitrate'].min().reset_index()
hevc_min_bitrate.rename(columns={'actual_bitrate': 'hevc_bitrate'}, inplace=True)

results = []

for seq in fhd_df['seq_name'].unique():
    seq_df = fhd_df[(fhd_df['seq_name'] == seq) & (fhd_df['preset'] == 2)]
    hevc_seq_df = hevc_min_bitrate[hevc_min_bitrate['seq_name'] == seq]
    
    for codec in seq_df['codec'].unique():
        if codec != 'libx265':
            codec_df = seq_df[seq_df['codec'] == codec]
            codec_min_bitrate = codec_df.groupby('vmaf_bin')['actual_bitrate'].min().reset_index()
            
            merged_df = pd.merge(codec_min_bitrate, hevc_seq_df, on='vmaf_bin', how='inner')
            merged_df['bitrate_savings_%'] = (merged_df['hevc_bitrate'] - merged_df['actual_bitrate']) / merged_df['hevc_bitrate'] * 100
            merged_df['seq_name'] = seq
            merged_df['codec'] = codec
            results.append(merged_df[['seq_name', 'vmaf_bin', 'codec', 'bitrate_savings_%']])

savings_df = pd.concat(results, ignore_index=True)

average_savings = savings_df.groupby(['seq_name', 'codec'])['bitrate_savings_%'].mean().reset_index()

overall_savings = savings_df.groupby('codec')['bitrate_savings_%'].mean().reset_index()

output_file_path = "bitrate_savings_FHD.txt"
with open(output_file_path, "w") as file:
    file.write("Dettagli risparmio bitrate per intervallo di VMAF:\n")
    file.write(savings_df.to_string(index=False))
    file.write("\n\nRisparmio medio di bitrate per sequenza e codec:\n")
    file.write(average_savings.to_string(index=False))
    file.write("\n\nRisparmio medio di bitrate complessivo per ogni codec:\n")
    file.write(overall_savings.to_string(index=False))

print(f"Risultati salvati in: {output_file_path}")
