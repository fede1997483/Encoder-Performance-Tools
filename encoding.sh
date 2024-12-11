#!/bin/bash

file_config="$2"
file_config_name_with_ext=$(basename "${file_config}")
file_config_name_no_ext="${file_config_name_with_ext%.*}"
file_config_extension="${file_config_name_with_ext##*.}"

if [ ! -f "${file_config}" ]; then
  echo "File di configurazione non trovato."
  exit 1
fi

if [ "${file_config_extension}" != "cfg" ]; then
  echo "Errore: estensione file di configurazione non corretta."
  exit 1
fi

. ./${file_config}

file_name=$1
file_name_ext=$(basename "$file_name")
file_name_no_ext="${file_name_ext%.*}"
width=$3
height=$4
fps=$5
vvc_preset="$VVC_PRESET"
vvc_enc_mode=$VVC_ENCODING_MODE

for arg in "$@"; do
  case "$arg" in
    bitrate=*)
      bit_rate_param="${arg}"
      BIT_RATES=${arg#*=}
      ;;
  esac
done

bit_rates_=$(echo "$BIT_RATES" | tr ' ' '_')

path_to_results="./results_${file_name_no_ext}_${file_config_name_no_ext}_${bit_rates_}/"


if [ "${ENCODE}" = "on" ]; then
  rm -rf ${path_to_results}
  mkdir -m 755 -p ${path_to_results}
  cp ${file_config} ${path_to_results}
fi

for codec in $CODECS; do
    echo "Processing file: ${file_name_ext} (codec: $codec)"
    sh ./encoding_scripts/encoding_bit_rate.sh $file_name $file_config $codec $width $height $fps $bit_rate_param
    echo "Encoding finished ($codec)."
done


if [ "${EVALUATE}" = "on" ]; then
  chmod +x ./vmaf
  sh ./vmaf_scripts/vmaf_bit_rate.sh $file_name $file_config $codec $width $height $fps $bit_rate_param

  if [ "${vvc_enc_mode}" = "ABR" ]; then
    mkdir -m 755 -p "${path_to_results}graphs"
    cd ./python_scripts/
    python3 vmaf.py "${CODECS}" "${BIT_RATES}" "${file_name_ext}" "${vvc_preset}" "${vvc_enc_mode}" "${path_to_results}"
    python3 psnr.py "${CODECS}" "${BIT_RATES}" "${file_name_ext}" "${vvc_preset}" "${vvc_enc_mode}" "${path_to_results}"
    cd ..
  fi
fi
