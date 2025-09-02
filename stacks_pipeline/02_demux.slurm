#!/bin/sh

#SBATCH --job-name=demux
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6
#SBATCH --mem=16GB
#SBATCH --time=20:00:00
#SBATCH --output=./logs/demux.out
#SBATCH --error=./logs/demux.err

# Source config variables
source ./config.sh

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate "$CONDA_ENV"

for fastq in ./fastq_trimmed/*_trimmed.fq.gz; do
    # Extract library, lane and flowcell info from filename of each trimmed .fq.gz file
    library=$(basename "$fastq" | cut -d'_' -f1)
    libraryprepid=${library:2}
    lane=$(basename "$fastq" | cut -d'_' -f4)
    flowcell=$(basename "$fastq" | cut -d'_' -f2)

    # Demultiplex tags, output to ./tags/
    process_radtags -f "$fastq" \
        -o ./tags/ \
        -b "./metadata/barcodes_${libraryprepid}.txt" \
        --renz_1 "$ENZYME_1" --renz_2 "$ENZYME_2" \
        -r -c -q \
        --inline-null \
        --threads 6

    # Rename demultiplexed tag files to the format <library>_<flowcell>_<lane>_<barcode>.fq.gz
    for sample in ./tags/sample_*; do
        mv "$sample" "./tags/$(basename "$sample" | sed "s/^sample_/${library}_${flowcell}_${lane}_/")"
    done
done