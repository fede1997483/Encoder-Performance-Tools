#!/bin/bash

# Verifica degli argomenti
if [ $# -ne 2 ]; then
  echo "Uso: $0 input_csv output_csv"
  exit 1
fi

input_csv=$1
output_csv=$2

# Funzione per convertire i preset in valori numerici
convert_preset() {
  codec=$1
  preset=$2
  case $codec in
    "libaom-av1")
      echo "$preset" # I preset AV1 sono già numerici
      ;;
    "libvvenc")
      case $preset in
        "faster") echo "5" ;;
        "fast") echo "4" ;;
        "medium") echo "3" ;;
        "slow") echo "2" ;;
        "slower") echo "1" ;;
        *) echo "$preset" ;;
      esac
      ;;
    "libx265")
      case $preset in
        "ultrafast") echo "8" ;;
        "superfast") echo "7" ;;
        "veryfast") echo "6" ;;
        "faster") echo "5" ;;
        "fast") echo "4" ;;
        "medium") echo "3" ;;
        "slow") echo "2" ;;
        "veryslow") echo "1" ;;
        "placebo") echo "0" ;;
        *) echo "Unknown" ;;
      esac
      ;;
    *)
      echo "$preset"
      ;;
  esac
}

# Lettura del file CSV e conversione dei preset
{
  read -r header
  echo "$header" > "$output_csv"
  while IFS=',' read -r seq_name fps duration w h bitrate codec preset vmaf psnr_y float_ssim real user sys actual_bitrate; do
    new_preset=$(convert_preset "$codec" "$preset")
    echo "$seq_name,$fps,$duration,$w,$h,$bitrate,$codec,$new_preset,$vmaf,$psnr_y,$float_ssim,$real,$user,$sys,$actual_bitrate" >> "$output_csv"
  done
} < "$input_csv"

echo "Conversione completata. File salvato in: $output_csv"
