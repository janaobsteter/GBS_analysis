# First run the cutadapt (run from the fasta dir - parallel)
cd 
common_adapter="AGATCGGAAGAGC"

for fastq in $(ls /home/share/GBS_honeybee/Run2/data/fastq/*fastq.gz)
do 
    echo  cutadapt -g AACCGGTT -m 50 \
    -o /home/share/GBS_honeybee/Run2/1_trimmed$(basename ${fastq%.fastq.gz})_trimmed.fastq.gz \
    ${fastq}
done

# Second - run demupliplexing with stacks

process_radtags -p /home/share/GBS_honeybee/Run2/data/fastq/ \
                -o /home/share/GBS_honeybee/Run2/2_demultiplexed/ \
                -b /home/share/GBS_honeybee/Run2/barcodes/Merged_barcodes.txt \
                --inline_null \
                --renz-1 mspI --renz-2 apeKI -r -c -q