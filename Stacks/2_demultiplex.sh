# We must demultiplex per library, because barcodes are duplicated across libraries
for library in  'SQ5221' 'SQ5222' 'SQ5223' 'SQ5224' 'SQ5225' 
do
    if [ -d /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/${library} ]; then
        rm -rf /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/${library}/*
    else
        mkdir /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/${library}
    fi
    echo process_radtags -p /home/share/GBS_honeybee/Run2/${library}.all.bee.MspI-ApeKI/fastq/ \
            -o /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/${library}/ \
            -b /home/share/GBS_honeybee/Run2/Stacks_pipeline/barcodes/${library}_barcodes.txt \
            --inline_null \
            --renz-1 mspI --renz-2 apeKI -r -c -q               
done | parallel