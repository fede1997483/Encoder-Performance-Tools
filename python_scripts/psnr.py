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
path_to_results = '../' + sys.argv[6] 

file_paths = {
    'AV1': {rate: Path(f'{path_to_results}/AV1/results_AV1_{rate}k.json') for rate in bit_rates},
    'VVC': {rate: Path(f'{path_to_results}/VVC/results_VVC_{rate}k.json') for rate in bit_rates},
    'HEVC': {rate: Path(f'{path_to_results}/HEVC/results_HEVC_{rate}k.json') for rate in bit_rates}
}

for codec, paths in file_paths.items():
    for bitrate, path in paths.items():
        print(f"Codec: {codec}, Bitrate: {bitrate}, File Path: {path}")

average_psnr_per_bitrate = {
    'AV1': {},
    'VVC': {},
    'HEVC': {}
}

def extract_psnr_data(file_path):
    s_psnr_y = 0
    n_frames = 0
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        frames = data['frames']

        for frame in frames:
            metrics = frame['metrics']
            psnr_y = metrics['psnr_y']
            s_psnr_y += psnr_y
            n_frames += 1

    average_psnr = s_psnr_y / n_frames if n_frames > 0 else 0
    return average_psnr

for codec in codecs:
    if codec in file_paths:
        for bitrate, file_path in file_paths[codec].items():
            average_psnr = extract_psnr_data(file_path)
            average_psnr_per_bitrate[codec][bitrate] = average_psnr
            print(f"[{codec}] Bitrate: {bitrate} kbps, PSNR_Y: {average_psnr}")


plt.figure(figsize=(6, 4))

bitrate_values = bit_rates

if 'HEVC' in codecs:
    plt.plot(bitrate_values, list(average_psnr_per_bitrate['HEVC'].values()), 'o-', label='PSNR HEVC')
if 'VVC' in codecs:
    plt.plot(bitrate_values, list(average_psnr_per_bitrate['VVC'].values()), 'o--', label='PSNR VVC')
if 'AV1' in codecs:
    plt.plot(bitrate_values, list(average_psnr_per_bitrate['AV1'].values()), 'o-.', label='PSNR AV1')

plt.xlabel('Bitrate (kbps)')
plt.ylabel('PSNR_Y')
plt.title('PSNR_Y in funzione del Bitrate')
plt.legend()

plt.savefig(path_to_results + "/graphs/PSNR.png")

output_psnr_file = os.path.join(path_to_results, "PSNR_results.txt")
with open(output_psnr_file, 'w') as psnr_file:
    for codec in codecs:
        if codec in file_paths:
            psnr_file.write(f"Codec: {codec}\n")
            for bitrate, file_path in file_paths[codec].items():
                average_psnr = extract_psnr_data(file_path)
                average_psnr_per_bitrate[codec][bitrate] = average_psnr
                psnr_file.write(f"Bitrate: {bitrate} kbps, PSNR_Y: {average_psnr}\n")
                print(f"[{codec}] Bitrate: {bitrate} kbps, PSNR_Y: {average_psnr}")
            psnr_file.write("\n")
