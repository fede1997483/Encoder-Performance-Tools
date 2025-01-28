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

        presets_0_2 = subset[subset['preset'].astype(int).isin([0, 1, 2])]['preset'].unique()
        presets_3_4 = subset[subset['preset'].astype(int).isin([3, 4])]
        higher_presets = subset[subset['preset'].astype(str).str.isdigit() & (subset['preset'].astype(int) >= 5)]

        # Grafici per preset 0, 1, 2
        for preset in presets_0_2:
            preset_data = subset[subset['preset'].astype(int) == int(preset)]

            for metric in metrics:
                plt.figure(figsize=(8, 6))

                codecs = preset_data['codec'].unique()
                style_index = 0

                for codec in codecs:
                    codec_data = preset_data[preset_data['codec'] == codec]
                    codec_data = codec_data.sort_values(by='actual_bitrate')

                    if not codec_data.empty:
                        label = f"{codec} (preset {preset})"
                        line_style = line_styles[style_index % len(line_styles)]
                        marker = markers[style_index % len(markers)]
                        style_index += 1

                        plt.plot(codec_data['actual_bitrate'], codec_data[metric],
                                 linestyle=line_style, marker=marker, label=label)

                plt.title(f"{seq} - Preset {preset} - {metric.upper()}")
                plt.xlabel("Actual Bitrate (kbps)")
                plt.ylabel(metric.upper())
                plt.legend(title="Codec", fontsize='small')
                plt.grid(True)

                output_dir = os.path.join(base_output_dir, f"Preset_{preset}", metric.upper())
                os.makedirs(output_dir, exist_ok=True)
                plot_file = os.path.join(output_dir, f"{seq}_Preset_{preset}_{metric.upper()}.png")
                plt.savefig(plot_file)
                plt.close()

        # Grafici per preset 3-4
        if not presets_3_4.empty:
            for metric in metrics:
                plt.figure(figsize=(8, 6))

                codecs = presets_3_4['codec'].unique()
                style_index = 0

                for codec in codecs:
                    codec_data = presets_3_4[presets_3_4['codec'] == codec]
                    codec_data = codec_data.sort_values(by='actual_bitrate')

                    if not codec_data.empty:
                        for preset in [3, 4]:
                            specific_preset_data = codec_data[codec_data['preset'].astype(int) == preset]
                            label = f"{codec} (preset {preset})"
                            line_style = line_styles[style_index % len(line_styles)]
                            marker = markers[style_index % len(markers)]
                            style_index += 1

                            plt.plot(specific_preset_data['actual_bitrate'], specific_preset_data[metric],
                                     linestyle=line_style, marker=marker, label=label)

                plt.title(f"{seq} - Preset 3-4 - {metric.upper()}")
                plt.xlabel("Actual Bitrate (kbps)")
                plt.ylabel(metric.upper())
                plt.legend(title="Codec", fontsize='small')
                plt.grid(True)

                output_dir = os.path.join(base_output_dir, "Preset_3-4", metric.upper())
                os.makedirs(output_dir, exist_ok=True)
                plot_file = os.path.join(output_dir, f"{seq}_Preset_3-4_{metric.upper()}.png")
                plt.savefig(plot_file)
                plt.close()

        # Grafici per preset >= 5
        if not higher_presets.empty:
            for metric in metrics:
                plt.figure(figsize=(8, 6))

                codecs = higher_presets['codec'].unique()
                style_index = 0

                for codec in codecs:
                    codec_data = higher_presets[higher_presets['codec'] == codec]
                    codec_data = codec_data.sort_values(by='actual_bitrate')

                    if not codec_data.empty:
                        presets = codec_data['preset'].unique()
                        for preset in presets:
                            specific_preset_data = codec_data[codec_data['preset'].astype(int) == preset]
                            label = f"{codec} (preset {preset})"
                            line_style = line_styles[style_index % len(line_styles)]
                            marker = markers[style_index % len(markers)]
                            style_index += 1

                            plt.plot(specific_preset_data['actual_bitrate'], specific_preset_data[metric],
                                     linestyle=line_style, marker=marker, label=label)

                plt.title(f"{seq} - Preset >= 5 - {metric.upper()}")
                plt.xlabel("Actual Bitrate (kbps)")
                plt.ylabel(metric.upper())
                plt.legend(title="Codec", fontsize='small')
                plt.grid(True)

                output_dir = os.path.join(base_output_dir, "Preset_5_and_above", metric.upper())
                os.makedirs(output_dir, exist_ok=True)
                plot_file = os.path.join(output_dir, f"{seq}_Preset_5_and_above_{metric.upper()}.png")
                plt.savefig(plot_file)
                plt.close()

    print(f"I grafici per preset sono stati salvati nella directory: {base_output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilizzo: python3 generate_plots_by_preset.py <file_csv>")
    else:
        csv_file = sys.argv[1]
        generate_plots_by_preset(csv_file)