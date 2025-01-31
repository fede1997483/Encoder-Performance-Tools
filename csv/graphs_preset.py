import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

def generate_plots_by_preset(csv_file):
    try:
        data = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Errore durante il caricamento del file CSV: {e}")
        return

    required_columns = {'seq_name', 'codec', 'preset', 'actual_bitrate', 'vmaf', 'psnr_y', 'float_ssim'}
    if not required_columns.issubset(data.columns):
        print(f"Il file CSV manca di una o più colonne richieste: {required_columns}")
        return

    base_output_dir = os.path.join(os.getcwd(), "plots_by_preset")
    os.makedirs(base_output_dir, exist_ok=True)

    sequences = data['seq_name'].unique()
    metrics = ['vmaf', 'psnr_y', 'float_ssim']
    line_styles = ['-', '--', '-.', ':']
    markers = ['o', 's', '^', 'D', 'x', '+']

    for seq in sequences:
        subset = data[data['seq_name'] == seq]

        # Separazione dei dati in base al preset
        presets_2 = subset[subset['preset'].astype(str) == '2']
        presets_3_4 = subset[subset['preset'].astype(str).str.isdigit() & subset['preset'].astype(int).isin([3, 4])]
        higher_presets = subset[
            subset['preset'].astype(str).str.isdigit() & (subset['preset'].astype(int) >= 5)
        ]

        for preset_group, preset_label in [
            (presets_2, "Preset_2"),
            (presets_3_4, "Preset_3-4"),
            (higher_presets, "Preset_5_and_above")
        ]:
            if preset_group.empty:
                continue

            # Creiamo una figura con layout 2 righe (2x2) 
            fig, axs = plt.subplots(2, 2, figsize=(18, 12))

            # Disabilita l'angolo in basso a destra
            axs[1, 1].axis('off')

            for metric_idx, metric in enumerate(metrics[:2]):  # Per le prime due metriche
                ax = axs[0, metric_idx]  # Prima riga, due colonne (0,0) e (0,1)
                codecs = preset_group['codec'].unique()
                style_index = 0
                added_labels = set()

                for codec in codecs:
                    codec_data = preset_group[preset_group['codec'] == codec]
                    codec_data = codec_data.sort_values(by='actual_bitrate')
                    presets = codec_data['preset'].unique()

                    for preset in presets:
                        specific_preset_data = codec_data[codec_data['preset'].astype(str) == str(preset)]
                        if specific_preset_data.empty:
                            continue

                        label = f"{codec} (preset {preset})"
                        if label in added_labels:
                            continue

                        line_style = line_styles[style_index % len(line_styles)]
                        marker = markers[style_index % len(markers)]
                        style_index += 1

                        # Plot nella sottotramma corretta
                        ax.plot(
                            specific_preset_data['actual_bitrate'],
                            specific_preset_data[metric],
                            linestyle=line_style,
                            marker=marker,
                            label=label,
                            linewidth=1.0  # Modifica qui lo spessore
                        )

                        added_labels.add(label)

                ax.set_title(f"{seq} - {preset_label} - {metric.upper()}")
                ax.set_xlabel("Actual Bitrate (kbps)")
                ax.set_ylabel(metric.upper())
                ax.grid(True)
                ax.legend(title="Codec", fontsize='small')

            # Per la terza metrica (posizionata sotto, al centro)
            ax = axs[1, 0]  # La terza metrica va nella parte inferiore sinistra (1,0)
            metric = metrics[2]  # La terza metrica
            codecs = preset_group['codec'].unique()
            style_index = 0
            added_labels = set()

            for codec in codecs:
                codec_data = preset_group[preset_group['codec'] == codec]
                codec_data = codec_data.sort_values(by='actual_bitrate')
                presets = codec_data['preset'].unique()

                for preset in presets:
                    specific_preset_data = codec_data[codec_data['preset'].astype(str) == str(preset)]
                    if specific_preset_data.empty:
                        continue

                    label = f"{codec} (preset {preset})"
                    if label in added_labels:
                        continue

                    line_style = line_styles[style_index % len(line_styles)]
                    marker = markers[style_index % len(markers)]
                    style_index += 1

                    # Plot nella sottotramma corretta
                    ax.plot(
                        specific_preset_data['actual_bitrate'],
                        specific_preset_data[metric],
                        linestyle=line_style,
                        marker=marker,
                        label=label,
                        linewidth=1.0  # Modifica qui lo spessore
                    )

                    added_labels.add(label)

            ax.set_title(f"{seq} - {preset_label} - {metric.upper()}")
            ax.set_xlabel("Actual Bitrate (kbps)")
            ax.set_ylabel(metric.upper())
            ax.grid(True)
            ax.legend(title="Codec", fontsize='small')

            # Salvataggio della figura combinata con la disposizione modificata
            output_dir = os.path.join(base_output_dir, preset_label)
            os.makedirs(output_dir, exist_ok=True)
            plot_file = os.path.join(output_dir, f"{seq}_{preset_label}_combined.png")
            plt.tight_layout()
            plt.savefig(plot_file)
            plt.close()

    print(f"I grafici per preset sono stati salvati nella directory: {base_output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilizzo: python3 generate_plots_by_preset.py <file_csv>")
    else:
        csv_file = sys.argv[1]
        generate_plots_by_preset(csv_file)
