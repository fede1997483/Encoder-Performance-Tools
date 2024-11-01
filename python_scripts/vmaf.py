import sys
import json
import matplotlib.pyplot as plt
from pathlib import Path
import os

codecs = sys.argv[1].split()
bit_rates = list(map(int, sys.argv[2].split()))
file_name = sys.argv[3]
file_name_no_ext = os.path.splitext(file_name)[0]
vvc_preset = sys.argv[4]
vvc_enc_mode = sys.argv[5]
#path_to_results = '../results_' + file_name_no_ext + '_' + vvc_preset + '_' + vvc_enc_mode \
#    + '_'+ sys.argv[1].replace(' ','_') + '_' + sys.argv[2].replace(' ', '_') + '_kbs'
path_to_results = '../' + sys.argv[6] 

file_paths = {
    'AV1': {rate: Path(f'{path_to_results}/AV1/results_AV1_{rate}k.json') for rate in bit_rates},
    'VVC': {rate: Path(f'{path_to_results}/VVC/results_VVC_{rate}k.json') for rate in bit_rates},
    'HEVC': {rate: Path(f'{path_to_results}/HEVC/results_HEVC_{rate}k.json') for rate in bit_rates}
}

for codec, paths in file_paths.items():
    for bitrate, path in paths.items():
        print(f"Codec: {codec}, Bitrate: {bitrate}, File Path: {path}")


average_vmaf_per_bitrate = {
    'AV1': {},
    'VVC': {},
    'HEVC': {}
}

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
        for bitrate, file_path in file_paths[codec].items():
            average_vmaf = extract_vmaf_data(file_path)
            average_vmaf_per_bitrate[codec][bitrate] = average_vmaf
            print(f"[{codec}] Bitrate: {bitrate} kbps, VMAF: {average_vmaf}")


plt.figure(figsize=(6, 4))

bitrate_values = bit_rates

if 'HEVC' in codecs:
    plt.plot(bitrate_values, list(average_vmaf_per_bitrate['HEVC'].values()), 'o-', label='VMAF HEVC', color='blue')
if 'VVC' in codecs:
    plt.plot(bitrate_values, list(average_vmaf_per_bitrate['VVC'].values()), 'o--', label='VMAF VVC', color='red')
if 'AV1' in codecs:
    plt.plot(bitrate_values, list(average_vmaf_per_bitrate['AV1'].values()), 'o-.', label='VMAF AV1', color='green')

plt.xlabel('Bitrate (kbps)')
plt.ylabel('VMAF')
plt.title('VMAF in funzione del Bitrate')
plt.legend()

plt.savefig(path_to_results+"/graphs/VMAF.png")

output_vmaf_file = os.path.join(path_to_results, "VMAF_results.txt")
with open(output_vmaf_file, 'w') as vmaf_file:
    for codec in codecs:
        if codec in file_paths:
            vmaf_file.write(f"Codec: {codec}\n")
            for bitrate, file_path in file_paths[codec].items():
                average_vmaf = extract_vmaf_data(file_path)
                average_vmaf_per_bitrate[codec][bitrate] = average_vmaf
                vmaf_file.write(f"Bitrate: {bitrate} kbps, VMAF: {average_vmaf}\n")
                print(f"[{codec}] Bitrate: {bitrate} kbps, VMAF: {average_vmaf}")
            vmaf_file.write("\n")


