#!/bin/bash

# Stop script on error
set -euo pipefail

# Run individual steps
echo "Running 01_trim.slurm"
time sbatch --wait 01_trim.slurm

echo "Running 02_demux.slurm"
time sbatch --wait 02_demux.slurm

echo "Running 03_align.slurm"
time sbatch --wait 03_align.slurm

echo "Running 04_merge.slurm"
time sbatch --wait 04_merge.slurm

echo "Running 05_gstacks.slurm"
time sbatch --wait 05_gstacks.slurm

echo "Running 06_populations.slurm"
time sbatch --wait 06_populations.slurm