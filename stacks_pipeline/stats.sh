#!/bin/bash

POP_DIR='./populations'
VCF="${POP_DIR}/populations.snps.vcf"

pv "$VCF" | vcftools --gzvcf - --freq2 --out "${POP_DIR}/frequency" --max-alleles 2 
pv "$VCF" | vcftools --gzvcf - --depth --out "${POP_DIR}/depth" 
pv "$VCF" | vcftools --gzvcf - --site-mean-depth --out "${POP_DIR}/depth" 
pv "$VCF" | vcftools --gzvcf - --missing-indv --out "${POP_DIR}/missing" 
pv "$VCF" | vcftools --gzvcf - --missing-site --out "${POP_DIR}/missing" 

sed -i 's/{FREQ}/FREQ/g' "${POP_DIR}/frequency.frq"