#!/bin/bash
#SBATCH --job-name=vvc_hevc
#SBATCH --mail-type=ALL
#SBATCH --mail-user=federico.baldassi@studenti.polito.it
#SBATCH --partition=global
#SBATCH --time=60:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --output=job_%j.log
#SBATCH --mem=3G
#SBATCH --workdir=/home/fbaldassi

file_path=$1
config_path=$2
bit_rate_param=$3
module load singularity/3.2.1
singularity exec ubuntu_vvc.sif bash -c "cd scripts && sh encoding.sh ../${file_path} ../${config_path} ${bit_rate_param}"

