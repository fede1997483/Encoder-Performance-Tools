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
pix_fmt="-p ${PIX_FMT_FOR_VMAF}"
bit_depth="-b ${BIT_DEPTH_FOR_VMAF}"
vvc_preset=$VVC_PRESET
vvc_enc_mode=$VVC_ENCODING_MODE
output_csv="./results_${file_name_no_ext}_${file_config_name_no_ext}.csv"

# Initialize CSV file with headers
echo "seq_name,fps,duration,w,h,bitrate,codec,preset,enc_duration,vmaf,psnr_y,float_ssim" > $output_csv

# Function to extract metadata from .y4m file
extract_y4m_metadata() {
  fps=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$file_name" | bc -l)
  width=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$file_name")
  height=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$file_name")
  duration=$(ffprobe -v error -select_streams v:0 -show_entries format=duration -of csv=p=0 "$file_name")
}

# Set encoding parameters
if [ "$file_extension" = "y4m" ]; then
  pix_fmt=""
  bit_depth=""
  fps=""
  duration=""
  width=""
  height=""
else
  width="-w $3"
  height="-h $4"
  pix_fmt="-p ${PIX_FMT_FOR_VMAF}"
  bit_depth="-b ${BIT_DEPTH_FOR_VMAF}"
  duration="N/A"
fi

path_to_results_base="./results_${file_name_no_ext}_${file_config_name_no_ext}/"

# Function to calculate average metrics from JSON file
calculate_averages() {
  json_file=$1
  vmaf_avg=$(jq '[.frames[].metrics.vmaf] | add / length' "$json_file")
  psnr_y_avg=$(jq '[.frames[].metrics.psnr_y] | add / length' "$json_file")
  float_ssim_avg=$(jq '[.frames[].metrics.float_ssim] | add / length' "$json_file")
  echo "$vmaf_avg,$psnr_y_avg,$float_ssim_avg"
}

# Encoding process for CBR mode
if [ ${VVC_ENCODING_MODE} = "CBR" ]; then
  for codec in $CODECS; do
    path_to_results="${path_to_results_base}$codec/"
    for rate in $BIT_RATES; do
        echo "_________________________________"
        echo "$codec (bit rate: $rate kbit/s)"
        ./vmaf --reference "$file_name" --distorted ${path_to_results}output_decoded_${codec}_${rate}k.${file_extension} \
          $width $height $pix_fmt $bit_depth \
          --model version=vmaf_float_v0.6.1 -o ${path_to_results}results_${codec}_${rate}k.json \
          --json --feature psnr --feature float_ssim
        echo "_________________________________"
        
        # Set enc_duration to zero
        enc_duration=0
        
        # Extract metadata only before writing to CSV
        if [ "$file_extension" = "y4m" ]; then
          extract_y4m_metadata
        fi

        # Calculate average metrics
        metrics=$(calculate_averages "${path_to_results}results_${codec}_${rate}k.json")
        
        # Write row to CSV
        echo "$file_name_no_ext,$fps,$duration,$width,$height,$rate,$codec,$vvc_preset,$enc_duration,$metrics" >> $output_csv

        # Reset values to empty
        fps=""
        duration=""
        width=""
        height=""
    done
  done
fi

# Encoding process for VBR mode
if [ ${VVC_ENCODING_MODE} = "VBR" ]; then
  for codec in $CODECS; do
    path_to_results="${path_to_results_base}$codec/"
    
    echo "_________________________________"
    echo "$codec (bit rate: $rate kbit/s)"
    ./vmaf --reference "$file_name" --distorted ${path_to_results}output_decoded_${codec}.${file_extension} \
      $width $height $pix_fmt $bit_depth \
      --model version=vmaf_float_v0.6.1 -o ${path_to_results}results_${codec}.json \
      --json --feature psnr --feature float_ssim
    echo "_________________________________"
    
    # Set enc_duration to zero
    enc_duration=0
    
    # Extract metadata only before writing to CSV
    if [ "$file_extension" = "y4m" ]; then
      extract_y4m_metadata
    fi

    # Calculate average metrics
    metrics=$(calculate_averages "${path_to_results}results_${codec}.json")
    
    # Write row to CSV
    echo "$file_name_no_ext,$fps,$duration,$width,$height,N/A,$codec,$vvc_preset,$enc_duration,$metrics" >> $output_csv

    # Reset values to empty
    fps=""
    duration=""
    width=""
    height=""
  done
fi
