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
    required_columns = {'seq_name', 'codec', 'preset', 'actual_bitrate', 'vmaf', 'psnr_y', 'float_ssim'}
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
                        plt.plot(codec_preset_data['actual_bitrate'], codec_preset_data[metric], marker='o', label=label)

            # Configurazione del grafico
            plt.title(f"{seq}_{metric.upper()}")
            plt.xlabel("Actual Bitrate (kbps)")
            plt.ylabel(metric.upper())
            plt.legend(title="Codec (Preset)", fontsize='small')
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
