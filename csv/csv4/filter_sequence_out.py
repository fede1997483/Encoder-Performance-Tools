import pandas as pd

# Percorso del file originale
file_path = 'out.csv'

# Caricamento del file CSV
df = pd.read_csv(file_path)

# Sequenze da eliminare
sequences_to_remove = [
    "Giftmord-SDR_8s_11_1920x1080",
    "Giftmord-SDR_8s_11_3840x2160",
    "big_buck_bunny_480p"
]

# Filtrare le righe che non contengono le sequenze da rimuovere
filtered_df = df[~df['seq_name'].isin(sequences_to_remove)]

# Salvataggio del nuovo file senza le sequenze specificate
output_file_path = 'cleaned_out.csv'
filtered_df.to_csv(output_file_path, index=False)

print(f"File salvato senza le sequenze specificate: {output_file_path}")
