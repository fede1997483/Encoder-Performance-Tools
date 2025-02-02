import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

import matplotlib.colors as mcolors

def generate_plots_by_sequence(csv_file):
    try:
        data = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Errore durante il caricamento del file CSV: {e}")
        return

    required_columns = {'seq_name', 'codec', 'preset', 'actual_bitrate', 'vmaf', 'psnr_y'}
    if not required_columns.issubset(data.columns):
        print(f"Il file CSV manca di una o più colonne richieste: {required_columns}")
        return

    base_output_dir = os.path.join(os.getcwd(), "plots_by_sequence")
    os.makedirs(base_output_dir, exist_ok=True)

    sequences = data['seq_name'].unique()
    metrics = ['vmaf', 'psnr_y']
    line_styles = ['-', '--', '-.', ':']  # Stile linea per codec
    markers = ['o', 's', '^', 'D', 'x', '+']  # Marker per preset
    colors = list(mcolors.TABLEAU_COLORS.values())  # Lista di colori predefiniti

    for seq in sequences:
        subset = data[data['seq_name'] == seq]
        codecs = subset['codec'].unique()
        presets = sorted(subset['preset'].astype(str).unique(), key=lambda x: int(x) if x.isdigit() else float('inf'))

        fig, axs = plt.subplots(2, 1, figsize=(10, 12))  # Disposizione verticale
        color_map = {codec: colors[i % len(colors)] for i, codec in enumerate(codecs)}  # Mappa codec -> colore

        for metric_idx, metric in enumerate(metrics):
            ax = axs[metric_idx]
            style_index = 0

            for codec in codecs:
                codec_data = subset[subset['codec'] == codec]
                line_style = line_styles[style_index % len(line_styles)]
                color = color_map[codec]
                style_index += 1
                
                marker_index = 0
                for preset in presets:
                    preset_data = codec_data[codec_data['preset'].astype(str) == preset]
                    if preset_data.empty:
                        continue
                    
                    preset_data = preset_data.sort_values(by='actual_bitrate')
                    marker = markers[marker_index % len(markers)]
                    marker_index += 1
                    
                    label = f"{codec} (preset {preset})"
                    ax.plot(
                        preset_data['actual_bitrate'],
                        preset_data[metric],
                        linestyle='',  # Rimuove la linea tra punti
                        marker=marker,
                        color=color,
                        label=label,
                        linewidth=1.0
                    )
                    ax.plot(
                        preset_data['actual_bitrate'],
                        preset_data[metric],
                        linestyle=line_style,  # Collega solo i punti consecutivi
                        marker='',
                        color=color,
                        linewidth=1.0
                    )
            
            ax.set_title(f"{seq} - {metric.upper()}")
            ax.set_xlabel("Actual Bitrate (kbps)")
            ax.set_ylabel(metric.upper())
            ax.grid(True)
            ax.legend(title="Codec / Preset", fontsize='small')

        plot_file = os.path.join(base_output_dir, f"{seq}_metrics.png")
        plt.tight_layout()
        plt.savefig(plot_file)
        plt.close()

    print(f"I grafici sono stati salvati nella directory: {base_output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilizzo: python3 generate_plots_by_sequence.py <file_csv>")
    else:
        csv_file = sys.argv[1]
        generate_plots_by_sequence(csv_file)
