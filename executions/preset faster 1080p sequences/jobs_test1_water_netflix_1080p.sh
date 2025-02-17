#!/bin/bash

sbatch script_3GB.sbatch ./seq_1080p/water_netflix_1080p.y4m ./configs/test1_config.cfg bitrate="8000"
sbatch script_3GB.sbatch ./seq_1080p/water_netflix_1080p.y4m ./configs/test1_config.cfg bitrate="12000"
sbatch script_3GB.sbatch ./seq_1080p/water_netflix_1080p.y4m ./configs/test1_config.cfg bitrate="16000"
sbatch script_3GB.sbatch ./seq_1080p/water_netflix_1080p.y4m ./configs/test1_config.cfg bitrate="20000"
sbatch script_3GB.sbatch ./seq_1080p/water_netflix_1080p.y4m ./configs/test1_config.cfg bitrate="24000"
sbatch script_3GB.sbatch ./seq_1080p/water_netflix_1080p.y4m ./configs/test1_config.cfg bitrate="28000"
sbatch script_3GB.sbatch ./seq_1080p/water_netflix_1080p.y4m ./configs/test1_config.cfg bitrate="32000"
sbatch script_3GB.sbatch ./seq_1080p/water_netflix_1080p.y4m ./configs/test1_config.cfg bitrate="36000"
sbatch script_3GB.sbatch ./seq_1080p/water_netflix_1080p.y4m ./configs/test1_config.cfg bitrate="40000"