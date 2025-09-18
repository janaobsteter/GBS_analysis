import pandas as pd

PEDIGREE_FILE = './metadata/pedigree.csv'

# Add FatherGroup and MotherGroup columns to pedigree
# (derived from location, year and role)
def add_parent_groups(sample):
    if sample['relationship'] == 'offspring':
        sample['FatherGroup'] = f'{sample['Location']}_{sample['year']}_dpc'
        sample['MotherGroup'] = f'{sample['Location']}_{sample['year']}_{sample['role']}'
        
    return sample

# Load full pedigree file
pedigree = pd.read_csv(PEDIGREE_FILE)

# Add parent groups, select columns
pedigree_KGD = pedigree.apply(add_parent_groups, axis=1).copy()
pedigree_KGD = pedigree_KGD[['IndivID', 'seqID', 'MotherID', 'FatherGroup', 'MotherGroup', 'relationship']]

# Keep queens and dpc, add ParGroup column (corresponds to MotherGroup and FatherGroup), select columns
groups_KGD = pedigree[pedigree['relationship'] != 'offspring'].copy()
groups_KGD['ParGroup'] = groups_KGD['Location'] + '_' + groups_KGD['year'].astype(str) + '_' + groups_KGD['role']
groups_KGD = groups_KGD[['IndivID', 'ParGroup']]

# Export to CSV
pedigree_KGD.to_csv('./metadata/pedigree_KGD.csv', index=False)
groups_KGD.to_csv('./metadata/groups_KGD.csv', index=False)