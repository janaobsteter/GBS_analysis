#!/bin/bash

#SBATCH --job-name=merge
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=16GB
#SBATCH --time=10:00:00
#SBATCH --output=./logs/merge.out
#SBATCH --error=./logs/merge.err

# Source config variables
source ./config.sh

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate "$CONDA_ENV"

# Construct a table of the format <sample-name>	<bam-file-name> for the .bam files in ./alignments/
table=''
for bam in ./alignments/*.bam; do
	# Extract library prep id, flowcell, lane and barcode from .bam file name
	libraryprepid=$(basename "$bam" | cut -d'_' -f1 | sed 's/^SQ//')
	flowcell=$(basename "$bam" | cut -d'_' -f2)
	lane=$(basename "$bam" | cut -d'_' -f3)
	barcode=$(basename "$bam" | cut -d'_' -f4 | cut -d'.' -f1)

	# Look up matching sample name in ./metadata/keyfile.tsv
	sample=$(awk -v libraryprepid="$libraryprepid" \
		-v lane="$lane" \
		-v barcode="$barcode" \
		-v flowcell="$flowcell" \
		"\$${FLOWCELL_COLUMN}==flowcell && \$${LANE_COLUMN}==lane && \$${BARCODE_COLUMN}==barcode && \$${LIBRARYPREPID_COLUMN}==libraryprepid {print \$${SAMPLE_COLUMN}}" \
		./metadata/keyfile.tsv)

	# Ignore files if a matching sample name can't be found
	if [[ $sample != '' ]]; then
		table+="$sample"$'\t'"$bam"$'\n'
	fi
done

# Write table
echo "$table" > ./metadata/sample_bam_table.tsv

# Process each unique sample name in the constructed table in parallel, 16 jobs at a time
cut -d'	' -f1 ./metadata/sample_bam_table.tsv | sort | uniq | grep -v '^$' \
| parallel -j 16 '
	# Capture the sample name from parallel and retrieve the list of bams related to it
	sample={}
	bams=$(grep "$sample" ./metadata/sample_bam_table.tsv | cut -d"	" -f2 | tr "\n" " ")

	# Merge all bams related to the same sample into one file <sample-name>_merged.bam
	samtools merge \
		-o "./samples_merged/${sample}_merged.bam" \
		$bams \
		-u

	# Add readgroups and output to ./samples/<sample-name>.bam
	# Sample names are used for all fields besides RGPL since gstacks doesnt like if a sample name appears in multiple readgroups
	samtools addreplacerg \
		-r "@RG\tID:${sample}\tLB:${sample}\tPL:ILLUMINA\tPU:${sample}\tSM:${sample}" \
		-o "./samples/${sample}.bam" \
		"./samples_merged/${sample}_merged.bam"

	# Index
	samtools index \
		"./samples/${sample}.bam"
'