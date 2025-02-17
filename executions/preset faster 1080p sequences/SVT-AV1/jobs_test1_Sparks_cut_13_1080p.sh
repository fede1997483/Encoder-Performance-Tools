#!/bin/bash

sbatch script_3GB.sbatch ./seq_1080p/Sparks_cut_13_1080p.y4m ./configs/test1_config_AV1-SVT.cfg bitrate="100"
sbatch script_3GB.sbatch ./seq_1080p/Sparks_cut_13_1080p.y4m ./configs/test1_config_AV1-SVT.cfg bitrate="300"
sbatch script_3GB.sbatch ./seq_1080p/Sparks_cut_13_1080p.y4m ./configs/test1_config_AV1-SVT.cfg bitrate="500"
sbatch script_3GB.sbatch ./seq_1080p/Sparks_cut_13_1080p.y4m ./configs/test1_config_AV1-SVT.cfg bitrate="700"
sbatch script_3GB.sbatch ./seq_1080p/Sparks_cut_13_1080p.y4m ./configs/test1_config_AV1-SVT.cfg bitrate="1000"
sbatch script_3GB.sbatch ./seq_1080p/Sparks_cut_13_1080p.y4m ./configs/test1_config_AV1-SVT.cfg bitrate="2000"
sbatch script_3GB.sbatch ./seq_1080p/Sparks_cut_13_1080p.y4m ./configs/test1_config_AV1-SVT.cfg bitrate="3000"
sbatch script_3GB.sbatch ./seq_1080p/Sparks_cut_13_1080p.y4m ./configs/test1_config_AV1-SVT.cfg bitrate="4000"
sbatch script_3GB.sbatch ./seq_1080p/Sparks_cut_13_1080p.y4m ./configs/test1_config_AV1-SVT.cfg bitrate="5000"