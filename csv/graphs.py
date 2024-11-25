import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def generate_plots(csv_file):
    # Carica il file CSV
    try:
        data = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Errore durante il caricamento del file CSV: {e}")
        return

    # Verifica che le colonne richieste siano presenti
    required_columns = {'seq_name', 'codec', 'actual_bitrate', 'vmaf', 'psnr_y', 'float_ssim'}
    if not required_columns.issubset(data.columns):
        print(f"Il file CSV manca di una o più colonne richieste: {required_columns}")
        return

    # Directory principale per i grafici
    base_output_dir = os.path.join(os.getcwd(), "plots")
    os.makedirs(base_output_dir, exist_ok=True)

    # Sequenze uniche
    sequences = data['seq_name'].unique()

    # Creazione dei grafici per ogni sequenza
    for seq in sequences:
        subset = data[data['seq_name'] == seq]
        
        # Metriche e codificatori unici
        metrics = ['vmaf', 'psnr_y', 'float_ssim']
        codecs = subset['codec'].unique()

        for metric in metrics:
            # Crea una sottocartella per ogni metrica
            metric_output_dir = os.path.join(base_output_dir, metric.upper())
            os.makedirs(metric_output_dir, exist_ok=True)

            plt.figure(figsize=(8, 6))

            for codec in codecs:
                codec_data = subset[subset['codec'] == codec]
                plt.plot(codec_data['actual_bitrate'], codec_data[metric], marker='o', label=codec)

            # Configurazione del grafico
            plt.title(f"{seq}_{metric.upper()}")
            plt.xlabel("Actual Bitrate (kbps)")
            plt.ylabel(metric.upper())
            plt.legend(title="Codec")
            plt.grid(True)

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
