import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("user_times.csv")

codec_colors = {
    "libx265": "blue",
    "libaom-av1": "darkorange",
    "libvvenc_1.12.1": "red",
    "libsvtav1": "green"
}

output_dir = "execution_time_graphs"
os.makedirs(output_dir, exist_ok=True)

unique_sequences = df["seq_name"].unique()

for seq in unique_sequences:
    subset = df[df["seq_name"] == seq]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for _, row in subset.iterrows():
        ax.bar(row["codec"], row["user"], color=codec_colors.get(row["codec"], "gray"), alpha=0.8)
    
    ax.set_ylabel("Tempo di codifica (ms)")
    ax.set_xlabel("Codec")
    ax.set_title(f"Sequenza: {seq}", fontsize=12)
    
    max_user = subset["user"].max()
    for i, row in enumerate(subset.itertuples()):
        ax.text(row.codec, row.user + max_user * 0.05, f"{row.user:.2f} ms\nVMAF: {row.vmaf:.2f}",
                ha='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.7), fontweight='bold')
        
    ax.set_ylim(0, max_user * 1.3)
    
    handles = [plt.Rectangle((0, 0), 1, 1, color=codec_colors[c]) for c in codec_colors]
    legend = fig.legend(handles, codec_colors.keys(), title="Codec", loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=2)
    
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    
    output_path = os.path.join(output_dir, f"{seq.replace(' ', '_')}_execution_time_histogram.png")
    plt.savefig(output_path, bbox_inches='tight')
    
    plt.close(fig)

