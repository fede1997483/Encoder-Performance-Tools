import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

def generate_plots(csv_file):
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
    base_output_dir = os.path.join(os.getcwd(), "plots_time_colors")
    os.makedirs(base_output_dir, exist_ok=True)

    # Sequenze uniche
    sequences = data['seq_name'].unique()

    # Creazione dei grafici per ogni sequenza
    for seq in sequences:
        subset = data[data['seq_name'] == seq]

        # Calcola il valore medio di 'user' per ogni codec nella sequenza corrente
        codec_means = subset.groupby('codec')['user'].mean()
        user_min, user_max = codec_means.min(), codec_means.max()
        norm = Normalize(vmin=user_min, vmax=user_max)  # Normalizza per la sequenza corrente basandosi sui valori medi per codec
        colormap = plt.cm.viridis.reversed()  # Inverti la colormap

        # Metriche e combinazioni di codec e preset
        metrics = ['vmaf', 'psnr_y', 'float_ssim']
        codecs = subset['codec'].unique()
        presets = subset['preset'].unique()

        for metric in metrics:
            # Crea una sottocartella per ogni metrica
            metric_output_dir = os.path.join(base_output_dir, metric.upper())
            os.makedirs(metric_output_dir, exist_ok=True)

            plt.figure(figsize=(8, 6))

            for codec in codecs:
                for preset in presets:
                    # Filtra i dati per codec e preset
                    codec_preset_data = subset[(subset['codec'] == codec) & (subset['preset'] == preset)]

                    # Ordina i dati per bitrate
                    codec_preset_data = codec_preset_data.sort_values(by='actual_bitrate')

                    # Plotta solo se ci sono dati
                    if not codec_preset_data.empty:
                        label = f"{codec} ({preset})"

                        # Determina il colore basato sul valore medio di 'user' per il codec
                        mean_user = codec_means[codec]
                        color = colormap(norm(mean_user))

                        plt.plot(codec_preset_data['actual_bitrate'], codec_preset_data[metric], marker='o', label=label, color=color)

            # Configurazione del grafico
            plt.title(f"{seq}_{metric.upper()}")
            plt.xlabel("Actual Bitrate (kbps)")
            plt.ylabel(metric.upper())
            plt.legend(title="Codec (Preset)", fontsize='small')
            plt.grid(True)

            # Aggiunge una barra colori per la leggibilità
            sm = ScalarMappable(cmap=colormap, norm=norm)
            sm.set_array([])  # Necessario per generare la colorbar
            cbar = plt.colorbar(sm, ax=plt.gca(), orientation='vertical')
            cbar.set_label('Execution Time (user)')

            # Salvataggio del grafico nella cartella specifica della metrica
            plot_file = os.path.join(metric_output_dir, f"{seq}_{metric.upper()}.png")
            plt.savefig(plot_file)
            plt.close()

    print(f"I grafici sono stati salvati nella directory: {base_output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilizzo: python3 generate_plots.py <file_csv>")
    else:
        csv_file = sys.argv[1]
        generate_plots(csv_file)