#!/bin/bash

file_config="$2"
file_config_name_with_ext=$(basename "${file_config}")
file_config_name_no_ext="${file_config_name_with_ext%.*}"
file_config_extension="${file_config_name_with_ext##*.}"
. ./${file_config}

file_name=$1
file_name_ext=$(basename "$file_name")
file_name_no_ext="${file_name_ext%.*}"
codec=$3
codecs_=$(echo "$CODECS" | tr ' ' '_')
file_extension="${file_name##*.}"
width=$4
height=$5
fps=$6
pix_fmt="-pix_fmt ${PIX_FMT_FOR_ENC_DEC}"
s="-s ${width}x${height}"
r="-r "$fps""
hevc_preset="$HEVC_PRESET"
vvc_preset="$VVC_PRESET"
av1_svt_preset="$AV1_PRESET"
svt_preset="$AV1_SVT_PRESET"
vvc_enc_mode=$VVC_ENCODING_MODE
ffmpeg_vvc_prmts=$FFMPEG_VVC_PARAMETERS
vvenc_prmts=$VVENC_PARAMETERS
ffmpeg_hevc_prmts=$FFMPEG_HEVC_PARAMETERS
hevc_prmts=$HEVC_PARAMETERS

for arg in "$@"; do
  case "$arg" in
    bitrate=*)
      BIT_RATES="${arg#*=}"
      ;;
  esac
done

bit_rates_=$(echo "$BIT_RATES" | tr ' ' '_')

path_to_results_base="./results_${file_name_no_ext}_${file_config_name_no_ext}_${bit_rates_}/"

if [ "${file_extension}" = "y4m" ]; then
  pix_fmt=""
  s=""
  r=""
fi

if [ "${vvenc_prmts}" != "" ]; then
  vvenc_prmts="-vvenc-params ${vvenc_prmts}"
fi

if [ "${hevc_prmts}" != "" ]; then
  hevc_prmts="-x265-params ${hevc_prmts}"
fi

if [ ${VVC_ENCODING_MODE} = "ABR" ]; then
  path_to_results="${path_to_results_base}$codec/"
  mkdir -m 755 -p ${path_to_results}
  for rate in $BIT_RATES; do
    echo "."
    if [ $codec = "HEVC" ]; then
      if [ "${ENCODE}" = "on" ]; then
        { time ffmpeg $s $r ${pix_fmt} -i $file_name -c:v libx265 -preset ${ffmpeg_hevc_prmts} ${hevc_preset} -b:v ${rate}k ${hevc_prmts} -f hevc ${path_to_results}output_${rate}k.h265 ; } 2>> ${path_to_results}execution_times_${rate}k.txt
      fi
      if [ "${DECODE}" = "on" ]; then
        ffmpeg -i ${path_to_results}output_${rate}k.h265 -pix_fmt ${PIX_FMT_FOR_ENC_DEC} ${path_to_results}output_decoded_HEVC_${rate}k.${file_extension} -loglevel error
      fi
    fi
    if [ $codec = "VVC" ]; then
      if [ "${ENCODE}" = "on" ]; then
        { time ffmpeg $s $r ${pix_fmt} -i $file_name -c:v libvvenc ${ffmpeg_vvc_prmts} -preset ${vvc_preset} -b:v ${rate}k ${vvenc_prmts} -f rawvideo ${path_to_results}output_${rate}k.266 ; } 2>> ${path_to_results}execution_times_${rate}k.txt
      fi
      if [ "${DECODE}" = "on" ]; then
        ffmpeg -i ${path_to_results}output_${rate}k.266 -pix_fmt ${PIX_FMT_FOR_ENC_DEC} ${path_to_results}output_decoded_VVC_${rate}k.${file_extension} -loglevel error
      fi
    fi
    if [ $codec = "AV1" ]; then
      if [ "${ENCODE}" = "on" ]; then
        { time ffmpeg $s $r ${pix_fmt} -i $file_name -c:v libaom-av1 -cpu-used ${av1_preset} -b:v ${rate}k -f ivf ${path_to_results}output_${rate}k.ivf ; } 2>> ${path_to_results}execution_times_${rate}k.txt
      fi
      if [ "${DECODE}" = "on" ]; then
        ffmpeg -i ${path_to_results}output_${rate}k.ivf -pix_fmt ${PIX_FMT_FOR_ENC_DEC} ${path_to_results}output_decoded_AV1_${rate}k.${file_extension} -loglevel error
      fi
    fi
    if [ $codec = "AV1-SVT" ]; then
      if [ "${ENCODE}" = "on" ]; then
        { time ffmpeg $s $r ${pix_fmt} -i $file_name -c:v libsvtav1 -preset ${av1_svt_preset} -b:v ${rate}k -f ivf ${path_to_results}output_${rate}k.ivf ; } 2>> ${path_to_results}execution_times_${rate}k.txt
      fi
      if [ "${DECODE}" = "on" ]; then
        ffmpeg -i ${path_to_results}output_${rate}k.ivf -pix_fmt ${PIX_FMT_FOR_ENC_DEC} ${path_to_results}output_decoded_AV1-SVT_${rate}k.${file_extension} -loglevel error
      fi
    fi
  done
fi

if [ ${VVC_ENCODING_MODE} = "VBR" ]; then
  path_to_results="${path_to_results_base}$codec/"
  mkdir -m 755 -p ${path_to_results}
  echo "."
  if [ $codec = "HEVC" ]; then
    if [ "${ENCODE}" = "on" ]; then
      { time ffmpeg $s $r ${pix_fmt} -i $file_name -c:v libx265 ${ffmpeg_hevc_prmts}-preset ${hevc_preset} ${hevc_prmts} -f hevc ${path_to_results}output.h265 ; } 2>> ${path_to_results}execution_times.txt
    fi
    if [ "${DECODE}" = "on" ]; then
      ffmpeg -i ${path_to_results}output.h265 -pix_fmt ${PIX_FMT_FOR_ENC_DEC} ${path_to_results}output_decoded_HEVC.${file_extension} -loglevel error
    fi
  fi
  if [ $codec = "VVC" ]; then
    if [ "${ENCODE}" = "on" ]; then
      { time ffmpeg $s $r ${pix_fmt} -i $file_name -c:v libvvenc ${ffmpeg_vvc_prmts} -preset ${vvc_preset} ${vvenc_prmts} -f rawvideo ${path_to_results}output.266 ; } 2>> ${path_to_results}execution_times.txt
    fi
    if [ "${DECODE}" = "on" ]; then
      ffmpeg -i ${path_to_results}output.266 -pix_fmt ${PIX_FMT_FOR_ENC_DEC} ${path_to_results}output_decoded_VVC.${file_extension} -loglevel error
    fi
  fi
  if [ $codec = "AV1" ]; then
    if [ "${ENCODE}" = "on" ]; then
      { time ffmpeg $s $r ${pix_fmt} -i $file_name -c:v libaom-av1 -cpu-used ${av1_preset} -f ivf ${path_to_results}output.ivf ; } 2>> ${path_to_results}execution_times.txt
    fi
    if [ "${DECODE}" = "on" ]; then
      ffmpeg -i ${path_to_results}output.ivf -pix_fmt ${PIX_FMT_FOR_ENC_DEC} ${path_to_results}output_decoded_AV1.${file_extension} -loglevel error
    fi
  fi
  if [ $codec = "AV1-SVT" ]; then
    if [ "${ENCODE}" = "on" ]; then
      { time ffmpeg $s $r ${pix_fmt} -i $file_name -c:v libsvtav1 -preset ${av1_svt_preset} -f ivf ${path_to_results}output_svt.ivf ; } 2>> ${path_to_results}execution_times_svt.txt
    fi
    if [ "${DECODE}" = "on" ]; then
      ffmpeg -i ${path_to_results}output_svt.ivf -pix_fmt ${PIX_FMT_FOR_ENC_DEC} ${path_to_results}output_decoded_AV1_SVT.${file_extension} -loglevel error
    fi
  fi
fi
