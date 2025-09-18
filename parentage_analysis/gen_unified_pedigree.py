import pandas as pd
import numpy as np

# Add a queen column to the run 1 pedigree
def add_queen(sample: pd.Series) -> pd.Series:
    if pd.notna(sample['MotherID']):
        sample['queen'] = pedigree1.loc[pedigree1['IndivID'] == sample['MotherID']].iloc[0]['Original sample']
    elif sample['biotype'] == 'queen':
        sample['queen'] = sample['Original sample']
    
    return sample

# Add a microlocation column to the pedigree
def add_microlocation(sample: pd.Series) -> pd.Series:
    if sample['relationship'] != 'sire':
        if sample['Location'] == 'vrata' and sample['year'] == 2022:
            try:
                sample['microlocation'] = microlocations.loc[microlocations['queen'] == sample['queen']].iloc[0]['microlocation']
                if pd.isna(sample['microlocation']):
                    sample['microlocation'] = -2 
            except IndexError:
                sample['microlocation'] = -2
            
            
        elif sample['Location'] == 'vrata' and sample['year'] == 2023:
            try:
                sample['microlocation'] = microlocations.loc[microlocations['queen'] == sample['queen']].iloc[0]['situation_Vrata']
                if pd.isna(sample['microlocation']):
                    sample['microlocation'] = 1
            except IndexError:
                sample['microlocation'] = 1
        else:
            sample['microlocation'] = 4
        
    return sample

# Pad the last segment of the extraction label to 3 zeroes
# Some extraction labels are padded and some aren't, so this is required so they match up
def pad_IndivID(indiv_id):
    if pd.notna(indiv_id):
        split = indiv_id.split('-')
        return '-'.join(split[:-1] + [split[-1].zfill(3)])
    else:
        return np.nan

# The run 2 pedigree file is missing the mother extraction label (IndivID in the final unified pedigree), which needs to be looked up
def add_mother_IndivID(sample: pd.Series) -> pd.Series:
    if pd.notna(sample['MotherID']):
        sample['MotherIndivID'] = pedigree2.loc[pedigree2['IndivID'] == sample['MotherID']].iloc[0]['extraction_label']
    else:
        sample['MotherIndivID'] = np.nan
        
    return sample

# Read CSVs
pedigree1 = pd.read_csv('./metadata/pedigree_full_run1.csv')
pedigree2 = pd.read_csv('./metadata/pedigree_full_run2.csv')

microlocations = pd.read_csv('metadata/beeconsel_samples_received_total_2025-09-08(Sheet1).csv', encoding='latin1')

# Add queen column, select and rename columns from the run 1 pedigree
pedigree1 = pedigree1.apply(add_queen, axis=1)
pedigree1 = pedigree1[['IndivID', 'DNA SampleID', 'MotherID', 'relationship', 'colony_uid', 'source', 'year', 'role', 'queen']]
pedigree1 = pedigree1.rename(columns={
    'DNA SampleID': 'seqID',
    'source': 'Location'
})

# Add mother IndivID column, select and rename columns from the run 2 pedigree
pedigree2 = pedigree2.apply(add_mother_IndivID, axis=1)
pedigree2 = pedigree2[['extraction_label', 'seqID', 'MotherIndivID', 'relationship', 'colony_uid', 'Location', 'year', 'role', 'queen']] 
pedigree2 = pedigree2.rename(columns={
    'extraction_label': 'IndivID',
    'MotherIndivID': 'MotherID'
})

# Concat
pedigree = pd.concat([pedigree1, pedigree2], ignore_index=True)

# Pad IndivIDs and convert the year column to ints
pedigree['IndivID'] = pedigree['IndivID'].apply(pad_IndivID)
pedigree['MotherID'] = pedigree['MotherID'].apply(pad_IndivID)
pedigree['year'] = pedigree['year'].astype(int)

# Add a microlocation column
pedigree = pedigree.apply(add_microlocation, axis=1)

# Export CSV
pedigree.to_csv('./metadata/pedigree.csv', index=False)