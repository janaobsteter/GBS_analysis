# Run the bwa for each demultiplexed fastq file
#!/bin/bash

for input in $(ls /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/Clean_fastq/*fq.gz)
do
    echo ${input}
    output=$(basename $input | sed 's/.fq.gz/.sam/g')
    index=/home/share/GBS_honeybee/Run2/data/reference/GCF_003254395.2_Amel_HAv3.1_genomic.fna
    bwa mem -t 8 ${index} ${input} \
    -k 19 -c 500 -O 0,0 -E 2,2 -T 10 > /home/share/GBS_honeybee/Run2/Stacks_pipeline/3_bwa/alignments_options/${output}
done