import pandas as pd

# Percorso del file di input
input_file = "out.csv"
output_file = "filtered_out.csv"

# Caricare il file CSV mantenendo il formato originale
df = pd.read_csv(input_file, dtype=str)

# Convertire le colonne numeriche per il filtraggio
df["actual_bitrate"] = pd.to_numeric(df["actual_bitrate"], errors="coerce")
df["vmaf"] = pd.to_numeric(df["vmaf"], errors="coerce")

# Applicare i filtri richiesti:
# 1. Eliminare le righe per la sequenza "Daydreamer" che hanno actual_bitrate superiore a 150000
df = df[~((df["seq_name"] == "Daydreamer_SDR_8s_3840x2160_8") & (df["actual_bitrate"] > 150000))]


# 2. Eliminare le righe per "vegetables_tuil_4k" con vmaf < 60 e actual_bitrate > 10000
df = df[~((df["seq_name"] == "vegetables_tuil_4k") & ((df["vmaf"] < 60) | (df["actual_bitrate"] > 10000)))]

# 3. Eliminare le righe per "water_netflix_4k" con actual_bitrate > 100000
df = df[~(df["actual_bitrate"] > 100000)]

# Salvare il file filtrato
df.to_csv(output_file, index=False, quoting=1)

print(f"File filtrato salvato come {output_file}")