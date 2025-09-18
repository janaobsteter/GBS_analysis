import pandas as pd
import numpy as np

# Add microlocation column to MS and MS_summary
def add_microlocation(sample: pd.Series) -> pd.Series:
    if sample['Location-Year'] == 'vrata-2022':
        try:
            sample['microlocation'] = microlocations.loc[microlocations['queen'] == sample['queen']].iloc[0]['microlocation']
            if pd.isna(sample['microlocation']):
                sample['microlocation'] = -2 
        except IndexError:
            sample['microlocation'] = -2
    elif sample['Location-Year'] == 'vrata-2023':
        try:
            sample['microlocation'] = microlocations.loc[microlocations['queen'] == sample['queen']].iloc[0]['situation_Vrata']
            if pd.isna(sample['microlocation']):
                sample['microlocation'] = 1
        except IndexError:
            sample['microlocation'] = 1
    else:
        sample['microlocation'] = 4
        
    return sample

# Load microlocations CSV
microlocations = pd.read_csv('metadata/beeconsel_samples_received_total_2025-09-08(Sheet1).csv', encoding='latin1')

# Load asssignments files, concat, add microlocations
deepforest_2022_MS = pd.read_excel('./MS/deepforest-2022_MS.xlsx', sheet_name='assignment')
deepforest_2022_MS['Location-Year'] = 'deepforest-2022'

vrata_2022_MS = pd.read_excel('./MS/vrata-2022_MS.xlsx', sheet_name='assignment')
vrata_2022_MS['Location-Year'] = 'vrata-2022'

vrata_2023_MS = pd.read_excel('./MS/vrata-2023_MS.xlsx', sheet_name='assignment')
vrata_2023_MS['Location-Year'] = 'vrata-2023'

MS = pd.concat([deepforest_2022_MS, vrata_2022_MS, vrata_2023_MS], ignore_index=True)
MS = MS.apply(add_microlocation, axis=1)

# Load summary files, concat, add microlocations, exclude empty rows
deepforest_2022_MS_summary = pd.read_excel('./MS/deepforest-2022_MS.xlsx', sheet_name='summary')
deepforest_2022_MS_summary['Location-Year'] = 'deepforest-2022'

vrata_2022_MS_summary = pd.read_excel('./MS/vrata-2022_MS.xlsx', sheet_name='summary')
vrata_2022_MS_summary['Location-Year'] = 'vrata-2022'

vrata_2023_MS_summary = pd.read_excel('./MS/vrata-2023_MS.xlsx', sheet_name='summary')
vrata_2023_MS_summary['Location-Year'] = 'vrata-2023'

MS_summary = pd.concat([deepforest_2022_MS_summary, vrata_2022_MS_summary, vrata_2023_MS_summary], ignore_index=True)
MS_summary = MS_summary.apply(add_microlocation, axis=1)
MS_summary = MS_summary[MS_summary['colony_uid'].notna()]

# Export to CSV
MS.to_csv('./MS/MS.csv', index=False)
MS_summary.to_csv('./MS/MS_summary.csv', index=False)