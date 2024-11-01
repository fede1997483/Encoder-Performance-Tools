#!/bin/bash

file_config="$2"
file_config_name_with_ext=$(basename "${file_config}")
file_config_name_no_ext="${file_config_name_with_ext%.*}"
file_config_extension="${file_config_name_with_ext##*.}"
. ./${file_config}


file_name=$1
file_name_ext=$(basename "$file_name")
file_name_no_ext="${file_name_ext%.*}"
bit_rates_=$(echo "$BIT_RATES" | tr ' ' '_')
codecs_=$(echo "$CODECS" | tr ' ' '_')
file_extension="${file_name##*.}"
width="-w $3"
height="-h $4"
pix_fmt="-p ${PIX_FMT_FOR_VMAF}"
fps=$6
bit_depth="-b ${BIT_DEPTH_FOR_VMAF}"
vvc_preset=$VVC_PRESET
vvc_enc_mode=$VVC_ENCODING_MODE
if [ "$file_extension" = "y4m" ]; then
  pix_fmt=""
  width=""
  height=""
  bit_depth=""
fi

path_to_results_base="./results_${file_name_no_ext}_${file_config_name_no_ext}/"

if [ ${VVC_ENCODING_MODE} = "CBR" ]; then
  for codec in $CODECS; do
  path_to_results="${path_to_results_base}$codec/"
    for rate in $BIT_RATES; do
        echo "_________________________________"
        echo "$codec (bit rate: $rate kbit/s)"
        ./vmaf --reference "$file_name" --distorted ${path_to_results}output_decoded_${codec}_${rate}k.${file_extension}\
          $width $height $pix_fmt $bit_depth\
          --model version=vmaf_float_v0.6.1 -o ${path_to_results}results_${codec}_${rate}k.json\
          --json --feature psnr --feature float_ssim
        echo "_________________________________"
    done
  done
fi

if [ ${VVC_ENCODING_MODE} = "VBR" ]; then
  for codec in $CODECS; do
    path_to_results="${path_to_results_base}$codec/"
    echo "_________________________________"
    echo "$codec (bit rate: $rate kbit/s)"
    ./vmaf --reference "$file_name" --distorted ${path_to_results}output_decoded_${codec}.${file_extension}\
      $width $height $pix_fmt $bit_depth\
      --model version=vmaf_float_v0.6.1 -o ${path_to_results}results_${codec}.json\
      --json --feature psnr --feature float_ssim
    echo "_________________________________"
  done
fi
