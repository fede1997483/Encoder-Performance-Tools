import pandas as pd
import numpy as np

# Caricare il file CSV
file_path = "out.csv"
df = pd.read_csv(file_path)

# Creare una colonna per raggruppare i VMAF in intervalli di ampiezza 1
df['vmaf_bin'] = df['vmaf'].apply(lambda x: int(np.floor(x)))

# Filtrare i dati per il codec HEVC (libx265) con il preset più lento (2)
hevc_df = df[(df['codec'] == 'libx265') & (df['preset'] == 2)]
hevc_min_bitrate = hevc_df.groupby(['seq_name', 'vmaf_bin'])['actual_bitrate'].min().reset_index()
hevc_min_bitrate.rename(columns={'actual_bitrate': 'hevc_bitrate'}, inplace=True)

# Creare una lista per i risultati
results = []

# Iterare su ciascuna sequenza video
for seq in df['seq_name'].unique():
    seq_df = df[(df['seq_name'] == seq) & (df['preset'] == 2)]
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

# Creare un DataFrame finale con i risultati
savings_df = pd.concat(results, ignore_index=True)

# Calcolare il risparmio di bitrate medio per ogni sequenza e codec
average_savings = savings_df.groupby(['seq_name', 'codec'])['bitrate_savings_%'].mean().reset_index()

# Calcolare il risparmio di bitrate medio complessivo per ogni codec
overall_savings = savings_df.groupby('codec')['bitrate_savings_%'].mean().reset_index()

# Salvare i risultati in un file di testo
output_file_path = "bitrate_savings.txt"

# Convertire il DataFrame in una stringa formattata
savings_text = savings_df.to_string(index=False)
average_savings_text = average_savings.to_string(index=False)
overall_savings_text = overall_savings.to_string(index=False)

# Scrivere il file di testo
with open(output_file_path, "w") as file:
    file.write("Dettagli risparmio bitrate per intervallo di VMAF:\n")
    file.write(savings_text)
    file.write("\n\nRisparmio medio di bitrate per sequenza e codec:\n")
    file.write(average_savings_text)
    file.write("\n\nRisparmio medio di bitrate complessivo per ogni codec:\n")
    file.write(overall_savings_text)

# Stampare il percorso del file salvato
print(f"Risultati salvati in: {output_file_path}")
