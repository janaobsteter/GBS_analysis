import pandas as pd
import numpy as np

# Count number of heterozygous loci for given drone from pedigree in vcf
def count_heterozygous_loci(drone: pd.Series) -> int:
    try:
        vcf[drone['SampleID'] + '_GT'] = vcf[drone['SampleID']].str.split(':').str[0]
    except KeyError:
        return pd.Series({
            'seqID': drone['SampleID'],
            'n_heterozygous': np.nan
        })
    
    return pd.Series({
        'seqID': drone['SampleID'],
        'n_heterozygous': vcf[drone['SampleID'] + '_GT'].isin(['0/1', '1/0']).sum()
    })

# Load VCF and pedigree
vcf = pd.read_csv('./vcf/populations.snps.filtered.vcf', sep='\t', skiprows=196)

pedigree = pd.read_csv('./metadata/Run2_Sample_ID.csv')

# Count heterozygous sites
drones = pedigree[pedigree['biotype'] == 'Drone']
n_heterozygous_loci_per_drone = drones.apply(count_heterozygous_loci, axis=1)

# Log stats
min_n_heterozygous_loci = n_heterozygous_loci_per_drone['n_heterozygous'].min()
max_n_heterozygous_loci = n_heterozygous_loci_per_drone['n_heterozygous'].max()
mean_n_heterozygous_loci = n_heterozygous_loci_per_drone['n_heterozygous'].mean()

total = vcf.shape[0]

print(f'The total number of loci was {total}.')
print(f'The mean number of heterozygous loci among drones was {mean_n_heterozygous_loci:.2f} ({(mean_n_heterozygous_loci/total) * 100:.2f}%).')
print(f'The lowest number of heterozygous loci among drones was {int(min_n_heterozygous_loci)} ({(min_n_heterozygous_loci/total) * 100:.2f}%).')
print(f'The highest number of heterozygous loci among drones was {int(max_n_heterozygous_loci)} ({(max_n_heterozygous_loci/total) * 100:.2f}%).')