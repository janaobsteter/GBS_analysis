echo "gstacks \\"

for bam in /home/share/GBS_honeybee/Run2/Stacks_pipeline/3_bwa/alignments/*_new.bam
do
  echo "   -B $bam \\"
done 

echo "-O /home/share/GBS_honeybee/Run2/Stacks_pipeline/4_gstacks -t 16"