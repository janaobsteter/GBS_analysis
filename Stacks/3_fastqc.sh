for library in   'SQ5221' 'SQ5222' 'SQ5223' 'SQ5224' 'SQ5225'
do
    echo ${library}
    mkdir /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/${library}/fastqc
    mkdir /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/${library}/multifastqc
    fastqc -t 8 /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/${library}/*.fq.gz \
           -o /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/${library}/fastqc/
    multiqc /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/${library}/fastqc \
            -o /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/${library}/multifastqc/
done