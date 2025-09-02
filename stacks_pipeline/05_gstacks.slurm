#!/bin/bash

#SBATCH --job-name=gstacks
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=12GB
#SBATCH --time=20:00:00
#SBATCH --output=./logs/gstacks.out
#SBATCH --error=./logs/gstacks.err

# Source config variables
source ./config.sh

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate "$CONDA_ENV"

# Construct a list of bams from both runs to pass to gstacks
bams=""
for bam in ./samples/*.bam ; do
    bams+="-B $bam "
done

# Run gstacks
gstacks $bams -O ./gstacks/ --threads 16