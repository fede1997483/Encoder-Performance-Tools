import csv

# Percorso del file originale e del file aggiornato
input_file = 'merged_results.csv'
output_file = 'merged_results_updated.csv'

# Legge il file CSV, sostituisce "libvvenc" con "libvvenc_1.12.1" e scrive un nuovo file
with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        updated_row = [cell.replace('libvvenc', 'libvvenc_1.12.1') for cell in row]
        writer.writerow(updated_row)

print(f"Le occorrenze di 'libvvenc' sono state sostituite con 'libvvenc_1.12.1'. Il file aggiornato è stato salvato come {output_file}.")
