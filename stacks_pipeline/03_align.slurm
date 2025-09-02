#!/bin/bash

#SBATCH --job-name=align
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=16GB
#SBATCH --time=10:00:00
#SBATCH --output=./logs/align.out
#SBATCH --error=./logs/align.err

# Source config variables
source ./config.sh

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate "$CONDA_ENV"

export REFERENCE

# Run 8 parallel jobs with 2 threads each
parallel -j 8 '
	# Align and sort each .fq.gz in ./tags/
	bwa-mem2 mem \
		"$REFERENCE" \
		"{}" \
		-t 2 \
	| samtools sort \
		-O BAM \
		-o "./alignments/$(basename "{}" | sed "s/\.fq\.gz$/.bam/g")" \
		-u \
		-@ 1
' ::: ./tags/SQ*.fq.gz
