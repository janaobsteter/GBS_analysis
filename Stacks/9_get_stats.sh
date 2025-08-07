invcf=$1
outdir=$2
vcf_basename=$(basename $invcf)

mkdir ${outdir}/stats

vcftools --gzvcf ${invcf} --site-mean-depth --out ${outdir}/stats/${vcf_basename}
vcftools --gzvcf ${invcf} --freq2 --out ${outdir}/stats/${vcf_basename}
vcftools --gzvcf ${invcf} --depth --out ${outdir}/stats/${vcf_basename}
vcftools --gzvcf ${invcf} --site-quality --out ${outdir}/stats/${vcf_basename}
vcftools --gzvcf ${invcf} --missing-site --out ${outdir}/stats/${vcf_basename}
vcftools --gzvcf ${invcf} --missing-indv --out ${outdir}/stats/${vcf_basename}

