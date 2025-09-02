#!/bin/bash

#SBATCH --job-name=index
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4GB
#SBATCH --time=2:00:00
#SBATCH --output=./logs/index.out
#SBATCH --error=./logs/index.err

# Source config variables
source config.sh

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate "$CONDA_ENV"

# Index
bwa-mem2 index "$REFERENCE"