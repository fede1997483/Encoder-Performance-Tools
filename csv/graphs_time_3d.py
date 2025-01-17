import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def generate_3d_plots(csv_file):
    # Carica il file CSV
    try:
        data = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Errore durante il caricamento del file CSV: {e}")
        return

    # Verifica che le colonne richieste siano presenti
    required_columns = {'seq_name', 'codec', 'preset', 'actual_bitrate', 'vmaf', 'psnr_y', 'float_ssim', 'user'}
    if not required_columns.issubset(data.columns):
        print(f"Il file CSV manca di una o più colonne richieste: {required_columns}")
        return

    # Directory principale per i grafici
    base_output_dir = os.path.join(os.getcwd(), "plots_3d")
    os.makedirs(base_output_dir, exist_ok=True)

    # Sequenze uniche
    sequences = data['seq_name'].unique()

    # Creazione dei grafici 3D per ogni sequenza
    for seq in sequences:
        subset = data[data['seq_name'] == seq]

        # Metriche e combinazioni di codec e preset
        metrics = ['vmaf', 'psnr_y', 'float_ssim']
        codecs = subset['codec'].unique()
        presets = subset['preset'].unique()

        for metric in metrics:
            # Crea una sottocartella per ogni metrica
            metric_output_dir = os.path.join(base_output_dir, metric.upper())
            os.makedirs(metric_output_dir, exist_ok=True)

            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')

            for codec in codecs:
                for preset in presets:
                    # Filtra i dati per codec e preset
                    codec_preset_data = subset[(subset['codec'] == codec) & (subset['preset'] == preset)]

                    # Ordina i dati per bitrate
                    codec_preset_data = codec_preset_data.sort_values(by='actual_bitrate')

                    # Plotta solo se ci sono dati
                    if not codec_preset_data.empty:
                        label = f"{codec} ({preset})"
                        x = codec_preset_data['actual_bitrate']
                        y = codec_preset_data[metric]
                        z = codec_preset_data['user']

                        # Traccia la linea 3D
                        ax.plot(x, y, z, marker='o', label=label)

            # Configurazione del grafico
            ax.set_title(f"{seq} - {metric.upper()}")
            ax.set_xlabel("Actual Bitrate (kbps)")
            ax.set_ylabel(metric.upper())
            ax.set_zlabel("Execution Time (user)")
            ax.legend(title="Codec (Preset)", fontsize='small')

            # Salvataggio del grafico nella cartella specifica della metrica
            plot_file = os.path.join(metric_output_dir, f"{seq}_{metric.upper()}_3D.png")
            plt.savefig(plot_file)
            plt.close()

    print(f"I grafici 3D sono stati salvati nella directory: {base_output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilizzo: python3 generate_3d_plots.py <file_csv>")
    else:
        csv_file = sys.argv[1]
        generate_3d_plots(csv_file)
