#!/bin/bash

#SBATCH --job-name=populations
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=16GB
#SBATCH --time=20:00:00
#SBATCH --output=./logs/populations.out
#SBATCH --error=./logs/populations.err

# Source config variables
source ./config.sh

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate "$CONDA_ENV"

# Run populations
populations -P ./gstacks/ \
    -O ./populations/ \
    --vcf \
    --hwe \
    --threads 16 