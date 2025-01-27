import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def generate_execution_time_histograms(csv_file):
    try:
        data = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Errore durante il caricamento del file CSV: {e}")
        return

    required_columns = {'seq_name', 'codec', 'preset', 'user'}
    if not required_columns.issubset(data.columns):
        print(f"Il file CSV manca di una o più colonne richieste: {required_columns}")
        return

    base_output_dir = os.path.join(os.getcwd(), "execution_time_histograms")
    os.makedirs(base_output_dir, exist_ok=True)

    sequences = data['seq_name'].unique()

    for seq in sequences:
        subset = data[data['seq_name'] == seq]

        avg_execution_time = subset.groupby(['codec', 'preset'])['user'].mean().reset_index()

        if not avg_execution_time.empty:
            plt.figure(figsize=(10, 6))

            codecs = avg_execution_time['codec'].unique()
            presets = sorted(avg_execution_time['preset'].unique())

            bar_width = 0.2
            positions = range(len(presets))

            for idx, codec in enumerate(codecs):
                codec_data = avg_execution_time[avg_execution_time['codec'] == codec]
                times = [codec_data[codec_data['preset'] == p]['user'].values[0] if p in codec_data['preset'].values else 0 for p in presets]

                plt.bar([p + idx * bar_width for p in positions], times, bar_width, label=codec)

            plt.title(f"Average Execution Time - {seq}")
            plt.xlabel("Preset")
            plt.ylabel("Average Execution Time (s)")
            plt.xticks([p + (bar_width * len(codecs)) / 2 for p in positions], presets)
            plt.legend(title="Codec", fontsize='small')
            plt.grid(axis='y', linestyle='--', alpha=0.7)

            plot_file = os.path.join(base_output_dir, f"{seq}_execution_time_histogram.png")
            plt.savefig(plot_file)
            plt.close()

    print(f"Gli istogrammi dei tempi di esecuzione medi sono stati salvati nella directory: {base_output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilizzo: python3 generate_execution_time_histograms.py <file_csv>")
    else:
        csv_file = sys.argv[1]
        generate_execution_time_histograms(csv_file)
