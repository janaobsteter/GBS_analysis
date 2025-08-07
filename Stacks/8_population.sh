input="//home/share/GBS_honeybee/Run2/Stacks_pipeline/4_gstacks"
output="/home/share/GBS_honeybee/Run2/Stacks_pipeline/5_population"
populations \
   -P ${input} \
   -O ${output} \
   -t 8 \
   --vcf 