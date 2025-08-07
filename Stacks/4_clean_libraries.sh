# Library SQ5225 was a re-run of falted samples - so the samples found here can be removed from other libraries
cut -f4 /home/share/GBS_honeybee/Run2/SQ5225.all.bee.MspI-ApeKI/blind/key/SQ5225_keyfile.txt > \
    /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/SQ5225_samples.txt

awk '{print $1".fq.gz"}' /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/SQ5225_samples.txt > \
     /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/SQ5225_fastq.txt

# Prepare a list of negative control/failed samples to remove
for library in 'SQ5221' 'SQ5222' 'SQ5223' 'SQ5224' #'SQ5225'
do 
    echo $library
    cd /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/${library}/
    mkdir Failed_Negative
    ls *NEG*  > Failed_Negative/Negative.txt
    ls *fq.gz | grep -Fwf /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/SQ5225_fastq.txt \
        > Failed_Negative/Failed.txt
    cat Failed_Negative/Failed.txt Failed_Negative/Negative.txt | sort | uniq > Failed_Negative/Failed_Negative.txt 
    mv -t Failed_Negative/ $(< Failed_Negative/Failed_Negative.txt)
    cd /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/
done

# Move all fasta to the same folder
for library in 'SQ5221' 'SQ5222' 'SQ5223' 'SQ5224' 'SQ5225'
do 
    echo $library
    cd /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/${library}/
    ls *fq.gz > /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/${library}_clean_fastq.txt
    sed "s/.fq.gz//g" /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/${library}_clean_fastq.txt > \
    /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/${library}_clean_samples.txt
    cd /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/
done

# Clean the key files
for library in 'SQ5221' 'SQ5222' 'SQ5223' 'SQ5224' 'SQ5225'
do 
    cd /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/
    grep -Fwf ${library}_clean_samples.txt \
    /home/share/GBS_honeybee/Run2/${library}.all.bee.MspI-ApeKI/blind/key/${library}_keyfile.txt > \
    ${library}_keyfile_clean_samples.txt
    head -n1 /home/share/GBS_honeybee/Run2/${library}.all.bee.MspI-ApeKI/blind/key/${library}_keyfile.txt > \
        Header.txt 
    cd /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/
done

#Move the fastq files to a common directory
mkdir /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/Clean_fastq
for library in 'SQ5221' 'SQ5222' 'SQ5223' 'SQ5224' 'SQ5225'
do 
    echo $library
    cd /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/${library}
    for fastq in $(ls *fq.gz)
    do
        ln -s /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/${library}/${fastq} \
        /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/Clean_fastq/${fastq}
    done
done

# Merge all lists
cd /home/share/GBS_honeybee/Run2/Stacks_pipeline/2_demultiplexed/
cat *clean_fastq.txt > All_clean_fastq.txt
all_wc=$( less All_clean_fastq.txt | wc -l )
uniq_wc=$( sort All_clean_fastq.txt  | uniq | wc -l )
if [ "$all_wc" -eq "$uniq_wc" ]; then
    echo "No duplicated fastq files"
else
    echo "Some fastq are still duplicated!"
fi
# Key file
cat *keyfile_clean_samples* > All_keyfile_clean_samples.txt
all_key_wc=$( less All_keyfile_clean_samples.txt | wc -l )
uniq_wc_2="$(($uniq_wc * 2))"
if [ "$uniq_wc_2" -eq "$all_key_wc" ]; then
    echo "Key file contains all the samples."
else
    echo "Mismatch between keyfile and samples!"
fi
cat Header.txt All_keyfile_clean_samples.txt > tmp && mv tmp All_keyfile_clean_samples.txt 
