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

echo "seq_name,fps,duration,w,h,bitrate,codec,preset,vmaf,psnr_y,float_ssim,real,user,sys" > $output_csv

extract_y4m_metadata() {
  fps=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$file_name" | bc -l)
  width=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$file_name")
  height=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$file_name")
  duration=$(ffprobe -v error -select_streams v:0 -show_entries format=duration -of csv=p=0 "$file_name")
}

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

calculate_averages() {
  json_file=$1
  vmaf_avg=$(jq '[.frames[].metrics.vmaf] | add / length' "$json_file")
  psnr_y_avg=$(jq '[.frames[].metrics.psnr_y] | add / length' "$json_file")
  float_ssim_avg=$(jq '[.frames[].metrics.float_ssim] | add / length' "$json_file")
  echo "$vmaf_avg,$psnr_y_avg,$float_ssim_avg"
}

extract_info_from_log() {
  log_file=$1
  real_time=$(grep "elapsed" "$log_file" | awk '{print $3}' | sed 's/elapsed//')
  user_time=$(grep "user" "$log_file" | awk '{print $1}' | sed 's/user//')
  sys_time=$(grep "sys" "$log_file" | awk '{print $2}' | sed 's/system//')

  case $codec in
    "AV1")
      codec_library="libaom-av1"
      ;;
    "VVC")
      codec_library="libvvenc"
      ;;
    "HEVC")
      codec_library="libx265"
      ;;
  esac

  echo "$real_time,$user_time,$sys_time,$codec_library"
}

if [ ${VVC_ENCODING_MODE} = "CBR" ]; then
  for codec in $CODECS; do
    path_to_results="${path_to_results_base}$codec/"
    for rate in $BIT_RATES; do
        echo "_________________________________"
        echo "$codec (bit rate: $rate kbit/s)"
        
        enc_info=$(extract_info_from_log "${path_to_results}execution_times_${rate}k.txt")
        real_time=$(echo $enc_info | cut -d',' -f1)
        user_time=$(echo $enc_info | cut -d',' -f2)
        sys_time=$(echo $enc_info | cut -d',' -f3)
        codec_library=$(echo $enc_info | cut -d',' -f4)

        ./vmaf --reference "$file_name" --distorted "${path_to_results}output_decoded_${codec}_${rate}k.${file_extension}" \
          $width $height $pix_fmt $bit_depth \
          --model version=vmaf_float_v0.6.1 -o "${path_to_results}results_${codec}_${rate}k.json" \
          --json --feature psnr --feature float_ssim
        echo "_________________________________"
        
        if [ "$file_extension" = "y4m" ]; then
          extract_y4m_metadata
        fi

        metrics=$(calculate_averages "${path_to_results}results_${codec}_${rate}k.json")
        
        echo "$file_name_no_ext,$fps,$duration,$width,$height,$rate,$codec_library,$vvc_preset,$metrics,$real_time,$user_time,$sys_time" >> $output_csv

        fps=""
        duration=""
        width=""
        height=""
    done
  done
fi

if [ ${VVC_ENCODING_MODE} = "VBR" ]; then
  for codec in $CODECS; do
    path_to_results="${path_to_results_base}$codec/"
    
    echo "_________________________________"
    echo "$codec (VBR)"
    
    enc_info=$(extract_info_from_log "${path_to_results}execution_times.txt")
    real_time=$(echo $enc_info | cut -d',' -f1)
    user_time=$(echo $enc_info | cut -d',' -f2)
    sys_time=$(echo $enc_info | cut -d',' -f3)
    codec_library=$(echo $enc_info | cut -d',' -f4)

    ./vmaf --reference "$file_name" --distorted "${path_to_results}output_decoded_${codec}.${file_extension}" \
      $width $height $pix_fmt $bit_depth \
      --model version=vmaf_float_v0.6.1 -o "${path_to_results}results_${codec}.json" \
      --json --feature psnr --feature float_ssim
    echo "_________________________________"
    
    if [ "$file_extension" = "y4m" ]; then
      extract_y4m_metadata
    fi

    metrics=$(calculate_averages "${path_to_results}results_${codec}.json")
    
    echo "$file_name_no_ext,$fps,$duration,$width,$height,N/A,$codec_library,$vvc_preset,$metrics,$real_time,$user_time,$sys_time" >> $output_csv

    fps=""
    duration=""
    width=""
    height=""
  done
fi
