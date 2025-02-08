import pandas as pd

# Percorso del file originale
file_path = 'merged_results_updated.csv'

# Caricamento del file CSV
df = pd.read_csv(file_path)

# Mappatura delle sequenze da modificare
sequence_name_changes = {
    "Sparks_cut_13": "Sparks_cut_13_4k",
    "Sparks_cut_15": "Sparks_cut_15_4K",
    "cutting_orange_tuil": "cutting_orange_tuil_4k",
    "water_netflix": "water_netflix_4k",
    "bigbuck_bunny_8bit": "bigbuck_bunny_8bit_4k",
    "vegetables_tuil": "vegetables_tuil_4k"
}

# Modifica dei nomi delle sequenze
df['seq_name'] = df['seq_name'].replace(sequence_name_changes)

# Salvataggio del nuovo file con i nomi aggiornati
output_file_path = 'modified_sequences.csv'
df.to_csv(output_file_path, index=False)

print(f"File salvato con i nomi delle sequenze modificati: {output_file_path}")

