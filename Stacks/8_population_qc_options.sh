input="//home/share/GBS_honeybee/Run2/Stacks_pipeline/4_gstacks/options"
output="/home/share/GBS_honeybee/Run2/Stacks_pipeline/5_population/options/QC"
populations \
   -P ${input} \
   -O ${output} \
   --min-maf  0.05 \
   --max-obs-het  0.5 \
   --min-gt-depth 10 \
   --hwe \
   -t 8 \
   --vcf 



