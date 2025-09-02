#!/bin/bash

#SBATCH --job-name=trim
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=8GB
#SBATCH --time=10:00:00
#SBATCH --output=./logs/trim.out
#SBATCH --error=./logs/trim.err

# Source config variables
source ./config.sh

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate "$CONDA_ENV"

# Run cutadapt on each .fq.gz in ./fastq/, output to ./fastq_trimmed/
for fastq in ./fastq/*.fq.gz; do
    filename=$(basename "$fastq")
    cutadapt -a "$ADAPTER" "$fastq" -o "./fastq_trimmed/${filename%.fq.gz}_trimmed.fq.gz" -j 8
done