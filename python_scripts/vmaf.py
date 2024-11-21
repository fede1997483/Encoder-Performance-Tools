import sys
import json
import matplotlib.pyplot as plt
from pathlib import Path
import os
import csv

codecs = sys.argv[1].split()
bit_rates = list(map(int, sys.argv[2].split()))
file_name = sys.argv[3]
file_name_no_ext = os.path.splitext(file_name)[0]
vvc_preset = sys.argv[4]
vvc_enc_mode = sys.argv[5]
path_to_results = '../' + sys.argv[6]
actual_bitrate_file = os.path.join(path_to_results, "actual_bitrate.txt")

file_paths = {
    'AV1': {rate: Path(f'{path_to_results}/AV1/results_AV1_{rate}k.json') for rate in bit_rates},
    'VVC': {rate: Path(f'{path_to_results}/VVC/results_VVC_{rate}k.json') for rate in bit_rates},
    'HEVC': {rate: Path(f'{path_to_results}/HEVC/results_HEVC_{rate}k.json') for rate in bit_rates}
}

actual_bitrates = {codec: {} for codec in codecs}

with open(actual_bitrate_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        codec = row['codec']
        rate = int(row['rate'])
        actual_bitrate = float(row['actual_bitrate'])
        if codec in actual_bitrates:
            actual_bitrates[codec][rate] = actual_bitrate

average_vmaf_per_bitrate = {codec: {} for codec in codecs}

def extract_vmaf_data(file_path):
    s_vmaf = 0
    n_frames = 0
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        frames = data['frames']
        for frame in frames:
            metrics = frame['metrics']
            vmaf = metrics['vmaf']
            s_vmaf += vmaf
            n_frames += 1
    average_vmaf = s_vmaf / n_frames if n_frames > 0 else 0
    return average_vmaf

for codec in codecs:
    if codec in file_paths:
        for nominal_bitrate, file_path in file_paths[codec].items():
            average_vmaf = extract_vmaf_data(file_path)
            actual_bitrate = actual_bitrates[codec].get(nominal_bitrate, nominal_bitrate)
            average_vmaf_per_bitrate[codec][actual_bitrate] = average_vmaf
            print(f"[{codec}] Actual Bitrate: {actual_bitrate} kbps, VMAF: {average_vmaf}")

plt.figure(figsize=(6, 4))

for codec in codecs:
    if codec in average_vmaf_per_bitrate:
        actual_bitrates_list = sorted(average_vmaf_per_bitrate[codec].keys())
        vmaf_values = [average_vmaf_per_bitrate[codec][bitrate] for bitrate in actual_bitrates_list]
        linestyle = 'o-' if codec == 'HEVC' else 'o--' if codec == 'VVC' else 'o-.'
        color = 'blue' if codec == 'HEVC' else 'red' if codec == 'VVC' else 'green'
        plt.plot(actual_bitrates_list, vmaf_values, linestyle, label=f'VMAF {codec}', color=color)

plt.xlabel('Bitrate (kbps)')
plt.ylabel('VMAF')
plt.title('VMAF in funzione del Bitrate')
plt.legend()

output_graph_dir = os.path.join(path_to_results, "graphs")
os.makedirs(output_graph_dir, exist_ok=True)
plt.savefig(os.path.join(output_graph_dir, "VMAF.png"))

output_vmaf_file = os.path.join(path_to_results, "VMAF_results.txt")
with open(output_vmaf_file, 'w') as vmaf_file:
    for codec in codecs:
        if codec in average_vmaf_per_bitrate:
            vmaf_file.write(f"Codec: {codec}\n")
            for actual_bitrate in sorted(average_vmaf_per_bitrate[codec].keys()):
                vmaf = average_vmaf_per_bitrate[codec][actual_bitrate]
                vmaf_file.write(f"Actual Bitrate: {actual_bitrate} kbps, VMAF: {vmaf}\n")
            vmaf_file.write("\n")
