import pandas as pd
import numpy as np
from plotnine import *
from matplotlib import colormaps
from matplotlib.colors import to_hex


class MSCompare:
    def __init__(
        self,
        pedigree_file='./metadata/pedigree.csv',
        GBS_file='./BothMatchesAnnotated.csv',
        GBS_summary_file='./stats/father_stats_by_colony.csv',
        MS_file='./MS/MS.csv',
        MS_summary_file='./MS/MS_summary.csv'
    ):

        # Load CSVs

        # Pedigree file
        self.pedigree = pd.read_csv(pedigree_file)

        # GBS data
        self.GBS = pd.read_csv(GBS_file)
        self.GBS_summary = pd.read_csv(GBS_summary_file)
        self.GBS_correct = self.GBS[self.GBS['Correct']]

        # MS data
        self.MS = pd.read_csv(MS_file)
        self.MS_summary = pd.read_csv(MS_summary_file)
        
        # Select eligible workers
        MS_annotated = self.MS.apply(self._add_eligible, axis=1)
        self.MS_workers_eligible = MS_annotated[(MS_annotated['biotype'] == 'worker_brood') & MS_annotated['worker_eligible']]
        
        # Get color map
        self.viridis = colormaps['viridis']
        

    # Compare determined fathers
    def compare_fathers(self):
        self.father_comparison = []

        # Loop through workers processed with GBS
        for _, GBS_worker in self.GBS_correct.iterrows():
            # Try to find matching MS worker, if fails, skip
            try:
                MS_worker = self.MS_workers_eligible.loc[self.MS_workers_eligible['sample_id3'] == GBS_worker['IndivID']].iloc[0]
            except IndexError:
                continue
            
            GBS_worker_father = GBS_worker['BestFatherMatch']
            
            # For MS workers without identified fathers, set MSFather to np.nan and Match to false
            if pd.isna(MS_worker['fathers']):
                self.father_comparison.append([GBS_worker['IndivID'], GBS_worker_father, np.nan, False])
                continue
            
            # Parse fathers from MS father string
            MS_worker_fathers = MS_worker['fathers'].split(',')
            
            # Compare GBS BestFatherMatch and first listed MS father
            # Tried with GBS_worker_father in MS_worker_fathers, same result
            matching = GBS_worker_father == MS_worker_fathers[0]
            self.father_comparison.append([GBS_worker['IndivID'], GBS_worker_father, MS_worker_fathers[0], matching])
        
        # Construct dataframe, so comparison can later be written to CSV
        self.father_comparison = pd.DataFrame(self.father_comparison, columns=['IndivID', 'GBSFather', 'MSFather', 'Match'])
            
    
    # Export father comparison to CSV
    def father_comparison_to_csv(self, filename='./stats/father_comparison.csv'):
        self.father_comparison.to_csv(filename, index=False)
        
        
    # Concatenate summaries for plotting
    def gen_joint_summary(self):
        # Prepare MS summary for concat (select columns, add microlocations, rename, add Method column)
        MS_summary_temp = self.MS_summary[['colony_uid', 'frac_workers_with_known_fathers', 'Location-Year', 'microlocation']].copy()
        MS_summary_temp['microlocation'] = MS_summary_temp['microlocation'].astype(int).astype(str) + ' ' + MS_summary_temp['colony_uid'].astype(int).astype(str)
        MS_summary_temp = MS_summary_temp.rename(columns={
            'frac_workers_with_known_fathers': 'ProportionMatched',
            'microlocation': 'microlocation_colony_uid'
        })
        MS_summary_temp['Method'] = 'MS'

        # Prepare GBS summary for concat (select columns, add Method column)
        GBS_summary_temp = self.GBS_summary[['colony_uid', 'ProportionMatched', 'Location-Year', 'microlocation_colony_uid']].copy()
        GBS_summary_temp['Method'] = 'GBS'

        # Concat, exclude colonies only processed with one method, exclude invalid entries
        self.summary = pd.concat([MS_summary_temp, GBS_summary_temp], ignore_index=True)
        self.summary = self.summary[self.summary.duplicated('colony_uid', keep=False)]
        self.summary = self.summary[self.summary['colony_uid'].notna()]
        self.summary = self.summary[self.summary['ProportionMatched'] != '/']
        self.summary['colony_uid'] = self.summary['colony_uid'].astype(int)
        self.summary['ProportionMatched'] = self.summary['ProportionMatched'].astype(float)
        
    
    # Concatenate father info for plotting
    def gen_joint_fathers(self):
        # Prepare GBS fathers (father_stats_per_colony) for concat (select columns, add Method column)
        GBS_fathers = self.GBS_summary[['colony_uid', 'NFathers', 'Location-Year', 'microlocation_colony_uid']].copy()
        GBS_fathers['Method'] = 'GBS'

        # Count identified fathers from MS data, add microlocation column, add Method column
        MS_fathers = self.MS_workers_eligible.groupby('colony_uid')[['fathers', 'Location-Year', 'microlocation']].apply(self._count_MS_fathers).reset_index()
        MS_fathers['microlocation_colony_uid'] = MS_fathers['microlocation'].astype(int).astype(str) + ' ' + MS_fathers['colony_uid'].astype(int).astype(str)
        MS_fathers.drop('microlocation', axis=1, inplace=True)
        MS_fathers['Method'] = 'MS'

        # Concat, exclude colonies only processed with one method, convert types
        self.fathers = pd.concat([GBS_fathers, MS_fathers], ignore_index=True)
        self.fathers['colony_uid'] = self.fathers['colony_uid'].astype(int)
        self.fathers = self.fathers[self.fathers.duplicated('colony_uid', keep=False)]
        self.fathers['NFathers'] = self.fathers['NFathers'].astype(int)


    # Plot proportion comparison
    def plot_proportion(self, filename_prefix='./plots/', filename_suffix='_proportion_comparison.png'):
        self.gen_joint_summary()
        
        # Plot each location-year combination separately
        for location_year in self.summary['Location-Year'].unique():
            plot = (
                ggplot(self.summary[self.summary['Location-Year'] == location_year], aes(
                    x='microlocation_colony_uid',
                    y='ProportionMatched',
                    fill='Method'
                    )
                ) +
                geom_col(
                    position='dodge',
                ) +
                theme(
                    axis_text_x=element_text(
                        angle=45, 
                    )
                ) +
                labs(
                    y='Proportion fathers identified',
                    x='Microlocation and colony UID',
                    title=location_year,
                ) +
                scale_fill_manual(values=[to_hex(self.viridis(i)) for i in np.linspace(0, 0.8, 2)])
            )
        
            plot.save(filename=f'{filename_prefix}{location_year}{filename_suffix}')
            
    
    # Plot number unique fathers comparison
    def plot_n_fathers(self, filename_prefix='./plots/', filename_suffix='_n_fathers_comparison.png'):
        self.gen_joint_fathers()
        
        # Plot each location-year combination separately
        for location_year in self.fathers['Location-Year'].unique():
            # Count number drones (for caption)
            drones_GBS = self.pedigree[self.pedigree['relationship'] == 'sire']
            n_drones_GBS = len(drones_GBS[(drones_GBS['Location'] + '-' + drones_GBS['year'].astype(str)) == location_year]['IndivID'].unique())
            
            drones_MS = self.MS[self.MS['role'] == 'dpc']
            n_drones_MS = len(drones_MS[drones_MS['Location-Year'] == location_year])
            
            
            plot = (
                ggplot(self.fathers[self.fathers['Location-Year'] == location_year], aes(
                    x='microlocation_colony_uid',
                    y='NFathers',
                    fill='Method'
                    )
                ) +
                geom_col(
                    position='dodge',
                ) +
                theme(
                    axis_text_x=element_text(
                        angle=45, 
                    )
                ) +
                labs(
                    y='Number unique fathers identified',
                    x='Microlocation and colony UID',
                    title=location_year,
                    caption=f'Number GBS drones: {n_drones_GBS}\nNumber MS drones: {n_drones_MS}'
                ) +
                scale_fill_manual(values=[to_hex(self.viridis(i)) for i in np.linspace(0, 0.8, 2)]) +
                scale_y_continuous(breaks=range(0, max(n_drones_GBS, n_drones_MS)))
            )
            
            plot.save(filename=f'{filename_prefix}{location_year}{filename_suffix}')
        
            
    # Add Eligible column based on queen-brood incompatibility, missing MS and missing queen genotypes
    @staticmethod
    def _add_eligible(worker: pd.Series) -> pd.Series:
        queen_brood_incompatibility = pd.notna(worker['queen-brood_incompatibilities'])
        missing_MS =  worker[['A0007', 'A0113', 'Ap043', 'B0124', 'Ap055']].eq('/').any()
        queen_missing_genotype = worker['fathers'] == 'queen_missing_genotype'
        
        worker['worker_eligible'] = not (queen_brood_incompatibility or missing_MS or queen_missing_genotype)
        
        return worker

    # Count number of fathers from MS summary
    @staticmethod
    def _count_MS_fathers(colony: pd.DataFrame) -> pd.Series:
        # Construct set of unique fathers per colony from workers' father strings
        fathers = set(
            father
            for father_string in colony['fathers'] if pd.notna(father_string)
            for father in father_string.split(',')
        )
        
        return pd.Series({
            'Location-Year': colony['Location-Year'].iloc[0],
            'NFathers': len(fathers),
            'microlocation': colony['microlocation'].iloc[0]
        })


if __name__ == '__main__':
    ms_compare = MSCompare()
    # ms_compare.compare_fathers()
    # ms_compare.father_comparison_to_csv()
    ms_compare.plot_proportion()
    ms_compare.plot_n_fathers()