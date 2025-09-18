import pandas as pd

# Read CSVs
both_matches = pd.read_csv('./BothMatches.csv')
pedigree = pd.read_csv('./Run2_Sample_ID.csv').set_index('SampleID')

# Check whether father was correctly identified and write to new Correct column
def add_correct(worker):
    worker_pedigree = pedigree.loc[worker['seqID']]
    father = pedigree.loc[worker['BestFatherMatch']]
    
    worker['Correct'] = worker_pedigree['queen'] == father['queen']
    
    return worker

# Check correctness and log stats
workers_annotated = both_matches.apply(add_correct, axis=1)
workers_annotated.to_csv('./workers_annotated.csv', index=False)

correct = len(workers_annotated[workers_annotated['Correct']])
total = len(workers_annotated)

print(f'The father was correctly identified for {correct}/{total} ({(correct/total) * 100:.2f}%) artificially inseminated workers.')