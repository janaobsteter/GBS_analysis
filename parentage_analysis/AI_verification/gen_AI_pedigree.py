import pandas as pd
import numpy as np


def add_seqID(sample):
    sample['seqID'] = seqID_list.loc[seqID_list['sample.ID'] == sample['sample ID']].iloc[0]['SampleID']
    return sample


def add_MotherID(sample):
    if sample['biotype'] == 'Worker':
        try:
            sample['MotherID'] = seqID_list.loc[(seqID_list['biotype'] == 'Queen') & (seqID_list['queen'] == sample['queen'])].iloc[0]['SampleID']
        except IndexError:
            sample['MotherID'] = sample['queen']
            
    return sample


# Read CSVs
AI_list = pd.read_csv('./AI_list.csv')
pedigree_full = pd.read_csv('./pedigree.csv')
seqID_list = pd.read_csv('./Run2_Sample_ID.csv')

# Filter out only AI samples and add a seqID column
AI = AI_list[AI_list['Location'] == 'AI']
AI = AI.apply(add_seqID, axis=1)

# Table to convert biotype to relationship
RELATIONSHIP = {
    'Worker': 'offspring',
    'Queen': 'dam',
    'Drone': 'sire'
}

# Add MotherID column to AI pedigree
pedigree_AI = AI.apply(add_MotherID, axis=1).copy()

# Select columns, give all workers the FatherGroup 'all' and the MotherGroup 'AI', add IndivID and relationship columns, rename
pedigree_AI = pedigree_AI[['seqID', 'MotherID', 'biotype']]
pedigree_AI['IndivID'] = pedigree_AI['seqID']
pedigree_AI['FatherGroup'] = np.where(
    pedigree_AI['biotype'] == 'Worker',
    'all',
    ''
)
pedigree_AI['MotherGroup'] = np.where(
    pedigree_AI['biotype'] == 'Worker',
    'AI',
    ''
)
pedigree_AI['biotype'] = pedigree_AI['biotype'].apply(lambda biotype: RELATIONSHIP[biotype])
pedigree_AI = pedigree_AI.rename(columns={
    'biotype': 'relationship'
})

# Select all non-AI drones and add to pedigree
other_drones = pedigree_full[pedigree_full['relationship'] == 'sire']
pedigree_AI = pd.concat([other_drones, pedigree_AI], ignore_index=True)

# Generate groups file, give ParGroup 'all' to all fathers and 'AI' to all mothers (only AI mothers are in the pedigree)
groups_AI = pedigree_AI[pedigree_AI['relationship'] != 'offspring'].copy()
groups_AI['ParGroup'] = groups_AI['relationship'].apply((lambda relationship: 'AI' if relationship == 'dam' else 'all'))
groups_AI = groups_AI[['IndivID', 'ParGroup']]

# Export to CSVs
pedigree_AI.to_csv('./pedigree_AI.csv', index=False)
groups_AI.to_csv('./groups_AI.csv', index=False)

