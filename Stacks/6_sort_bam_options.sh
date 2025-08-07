
cd /home/share/GBS_honeybee/Run2/Stacks_pipeline/3_bwa/alignments_options

for sam_file in $(ls *sam)
do
    # Convert sam to bam
    samtools view --threads 4 -b -o ${sam_file%.*}.bam ${sam_file}
    # Sort
    samtools sort -o ${sam_file%.*}_sorted.bam -T ${sam_file%.*}_temp ${sam_file%.*}.bam

    # Add read group with picard
    index=/home/share/GBS_honeybee/Run2/data/reference/GCF_003254395.2_Amel_HAv3.1_genomic.fna
    bam_file="${sam_file%.*}_sorted.bam"
    RGSM=$(basename $bam_file | rev | cut -f 2- -d "_" | rev )
    RGLB="${RGSM}-L001"
    RGPU=001
    echo -e "$RGSM\t$RGLB\t$RGPU"

    java -Xmx50G -jar /home/jana/github/picard/build/libs/picard.jar AddOrReplaceReadGroups \
        I=${bam_file} \
        O=${bam_file%.*}_new.bam \
        RGID=$RGSM \
        RGLB=$RGLB \
        RGPL=ILLUMINA \
        RGPU=$RGPU \
        RGSM=$RGSM
done