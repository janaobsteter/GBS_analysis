# Scripts
## General
Can be reused for other datasets.
### `gen_KGD_pedigree.py`: 
- Generates KGD specific pedigree and groups files from unified pedigree.
- Input: `metadata/pedigree.csv`
- Output: `metadata/pedigree_KGD.csv`, `metadata/groups_KGD.csv`

### `ParPlot.py`:
- Performs some sanity checks and draws plots from KGD results.
- Input: `BothMatches.csv`, `metadata/pedigree.csv`, `metadata/groups_KGD.csv`, `metadata/pedigree_KGD.csv`
- Output: `stats/father_stats_by_location_year.csv`, `stats/father_stats_by_colony.csv`, `BothMatchesAnnotated.csv` + plots

## Project-specific
Need to be rewritten/modified for each dataset.

### `MSCompare.py`:
- Compares father matches between GBS and MS data, draws comparison plots.
- Input: `MS/MS.csv`, `MS/MS_summary.csv`, `stats/father_stats_by_colony.csv`, `BothMatchesAnnotated.csv`, `metadata/pedigree.csv`
- Output: `stats/father_comparison.csv` + plots

### `gen_unified_pedigree.py`:
- Generates unified pedigree file from run 1 and 2 pedigree files.
- Input: `metadata/pedigree_full_run1.csv`, `metadata/pedigree_full_run2.csv`
- Output: `metadata/pedigree.csv`

### `merge_MS.py`:
- Merges MS parentage data from multiple files.
- Input: `MS/deepforest-2022_MS.xlsx`, `MS/vrata-2022_MS.xlsx`, `MS/vrata-2023_MS.xlsx`
- Output: `MS/MS.csv`, `MS/MS_summary.csv`

### `plot_MS_patrilines.py`:
- Plots the estimated number of patrilines from MS data.
- Input: `MS/vrata-2022_MS_patrilines.xlsx`, `MS/vrata-2023_MS_patrilines.xlsx`, `MS/deepforest-2022_MS_patrilines.xlsx`
- Output: plots

### `check_drone_homozygous.py`:
- Counts the number of heterozygous loci for each drone
- Input: `./vcf/populations.snps.filtered.vcf`, `./metadata/Run2_Sample_ID.csv`

# Setup for general scripts

- Copy scripts into KGD directory
- Run `folders.sh` to create folders
- Copy or symlink unified pedigree file to `metadata/pedigree.csv` or change filename in scripts (for `gen_KGD_pedigree.py`, change `PEDIGREE_FILE`, for `ParPlot.py` specify `pedigree_file` in `ParPlot` instantiation)
- Copy vcf to `vcf/` (or somewhere else) and modify `genofile` in `GBSRun.R`
- Run `gen_KGD_pedigree.py`
- Run `GBSRun.R`
- Run `ParPlot.py`

# Unfied pedigree format

The unified pedigree file has the following columns:

| Column | Description |
|--------|-------------|
| IndivID | Individual specific unique identifier |
| seqID | Sample identifier used in vcf |
| MotherID | IndivID of mother, empty for sire and dam |
| relationship | offspring, dam or sire |
| colony_uid | Unique colony identifier |
| Location | Location where sample was collected |
| year | Year when sample was collected |
| role | mating_nuc, observation_nuc or dpc |
| microlocation | Microlocation info for plotting |
| queen | Queen ID, not required |

Example:
```
IndivID,Location,MotherID,colony_uid,microlocation,queen,relationship,role,seqID,year
E22/3-009,flatlands,,11,,,sire,dpc,M57571,2021
E22/3-009,flatlands,,11,,,sire,dpc,M57572,2021
E23/05-013,deepforest,,398,4,Q711,dam,mating_nuc,M56591,2022
E23/05-013,deepforest,,398,4,Q711,dam,mating_nuc,M56592,2022
E22/43-001,deepforest,E23/05-013,398,4,Q711,offspring,mating_nuc,M56593,2022
E22/43-002,deepforest,E23/05-013,398,4,Q711,offspring,mating_nuc,M56594,2022
```
