import pandas as pd
import numpy as np
from plotnine import *
from matplotlib import colormaps
from matplotlib.colors import to_hex

class ParPlot:
    def __init__(
        self, 
        pedigree_file='./metadata/pedigree.csv',
        kgd_pedigree_file='./metadata/pedigree_KGD.csv', 
        groups_file='./metadata/groups_KGD.csv', 
        both_matches_file='./BothMatches.csv'
    ):
        # Load CSVs
        self.pedigree = pd.read_csv(pedigree_file)
        self.pedigree_KGD = pd.read_csv(kgd_pedigree_file)
        self.both_matches = pd.read_csv(both_matches_file)
        self.groups_KGD = pd.read_csv(groups_file)
        
        # Add Correct column
        self.workers_annotated = self.both_matches[self.both_matches['MotherAssign'].isin(['Y', 'B'])].apply(self._add_correct, axis=1)


    # Log info
    def log_correct(self):
        n_correct = len(self.workers_annotated[self.workers_annotated['Correct']])
        
        total = len(self.workers_annotated)
        print(f'{n_correct}/{total} ({n_correct/total * 100:.1f}%) mother matches were correct.')


    # Check whether father matches are from the correct locations
    def check_father_groups(self):
        father_group_correct = self.both_matches.apply(self._father_group_correct, axis=1)
        
        if any(~father_group_correct):
            print('Warning: some fathers were matched outside their location.')


    def gen_father_stats(self):
        # Select only workers with correctly identified mothers
        correct = self.workers_annotated[self.workers_annotated['Correct']]
        
        # Group by colony (using BestMotherMatch as identifier)
        colonies = correct.groupby('BestMotherMatch')
        
        # Generate father stats by colony
        self.father_stats_by_colony = colonies[['FatherAssign', 'BestFatherMatch']].apply(self._colony_father_stats).reset_index()
        
        # Add location, year, colony uid, and microlocation info
        mothers = self.father_stats_by_colony['BestMotherMatch'].apply(lambda mother_match: self.pedigree.loc[self.pedigree['IndivID'] == mother_match].iloc[0])
        self.father_stats_by_colony['colony_uid'] = mothers['colony_uid']
        self.father_stats_by_colony['Location'] = mothers['Location']
        self.father_stats_by_colony['Year'] = mothers['year']
        self.father_stats_by_colony['Location-Year'] = self.father_stats_by_colony['Location'] + '-' + self.father_stats_by_colony['Year'].astype(str)
        self.father_stats_by_colony['microlocation_colony_uid'] = mothers['microlocation'].astype(int).astype(str) + ' ' + self.father_stats_by_colony['colony_uid'].astype(str)
        
        # Generate father stats by location-year
        self.father_stats_by_location_year = (
            self.father_stats_by_colony.groupby('Location-Year')[['NFathers', 'ProportionMatched']]
            .apply(self._location_year_father_stats)
            .reset_index()
        )


    # Write stats tables to CSVs
    def father_stats_to_csv(
        self,
        father_stats_by_location_year_file='./stats/father_stats_by_location_year.csv',
        father_stats_by_colony_file='./stats/father_stats_by_colony.csv'
    ):
        self.gen_father_stats()
        self.father_stats_by_location_year.to_csv(father_stats_by_location_year_file, index=False)
        self.father_stats_by_colony.to_csv(father_stats_by_colony_file, index=False)


    # Save matches with correctness info to CSV
    def workers_annotated_to_csv(self, filename='BothMatchesAnnotated.csv'):
        self.workers_annotated.to_csv(filename, index=False)


    def plot(
        self,
        proportion_fathers_per_colony_file='./plots/proportion_fathers_per_colony.png',
        n_fathers_per_colony_file='./plots/n_fathers_per_colony.png',
        proportion_fathers_per_location_year_file='./plots/proportion_fathers_per_location_year.png',
        n_fathers_per_location_year_file='./plots/n_fathers_per_location_year.png'
    ):
        
        self.gen_father_stats()
        
        # Define plots
        viridis = colormaps['viridis']
        
        # Count number of unique location-year combinations (for color palette)
        n_location_year = len(self.father_stats_by_colony['Location-Year'].unique())
        
        proportion_fathers_per_colony_plot = (
            ggplot(self.father_stats_by_colony, aes(x='microlocation_colony_uid', y='ProportionMatched', fill='Location-Year')) +
            geom_col(width=0.8) +
            labs(
                x='Microlocation and colony UID',
                y='Proportion fathers identified',
                fill='Location and year'
            ) +
            theme(
                axis_text_x=element_text(
                    angle=90, 
                    hjust=1.4,
                    size=7,
                ),
                legend_key_size=7,
                legend_title=element_text(size=7),
                legend_text=element_text(size=7) 
            ) +
            ylim(0, 1) +
            scale_fill_manual(values=[to_hex(viridis(i)) for i in np.linspace(0, 0.8, n_location_year)])
        )
        
        n_fathers_per_colony_plot = (
            ggplot(self.father_stats_by_colony, aes(x='microlocation_colony_uid', y='NFathers', fill='Location-Year')) +
            geom_col(width=0.8) +
            labs(
                x='Microlocation and colony UID',
                y='Number fathers identified',
                fill='Location and year'
            ) +
            theme(
                axis_text_x=element_text(
                    angle=90, 
                    hjust=1.4,
                    size=7,
                ),
                legend_key_size=7,
                legend_title=element_text(size=7),
                legend_text=element_text(size=7) 
            ) +
            scale_fill_manual(values=[to_hex(viridis(i)) for i in np.linspace(0, 0.8, n_location_year)])
        )
        
        proportion_fathers_per_location_year_plot = (
            ggplot(self.father_stats_by_location_year, aes(x='Location-Year', y='MeanProportionMatched')) +
            geom_col() +
            geom_errorbar(aes(ymin='MinProportionMatched', ymax='MaxProportionMatched')) +
            xlab('Location and year') +
            ylab('Mean proportion fathers identified') +
            ylim(0, 1) 
        )
        
        n_fathers_per_location_year_plot = (
            ggplot(self.father_stats_by_location_year, aes(x='Location-Year', y='MeanNFathers')) +
            geom_col() +
            geom_errorbar(aes(ymin='MinNFathers', ymax='MaxNFathers')) +
            xlab('Location and year') +
            ylab('Mean number fathers identified')
        )
        
        # Save plots
        proportion_fathers_per_colony_plot.save(filename=proportion_fathers_per_colony_file)
        n_fathers_per_colony_plot.save(filename=n_fathers_per_colony_file)
        proportion_fathers_per_location_year_plot.save(filename=proportion_fathers_per_location_year_file)
        n_fathers_per_location_year_plot.save(filename=n_fathers_per_location_year_file)


    # Check whether mothers were correctly identified, write to new Correct column
    def _add_correct(self, worker: pd.Series) -> pd.Series:
        # Retrieve correct mother from pedigree
        mother_id = self.pedigree.loc[self.pedigree['IndivID'] == worker['IndivID']].iloc[0]['MotherID']
        
        # Check whether mother was correctly matched and write to Correct
        worker['Correct'] = worker['BestMotherMatch'] == mother_id
            
        return worker


    # Generate per colony father stats
    @staticmethod
    def _colony_father_stats(colony: pd.DataFrame) -> pd.Series:
        father_matches = colony[colony['FatherAssign'].isin(['Y', 'B'])]
        fathers = list(father_matches['BestFatherMatch'].drop_duplicates())
        
        n_workers = len(colony)
        n_matched = len(father_matches)
        
        return pd.Series({
            'Fathers': fathers,
            'NFathers': len(fathers),
            'NWorkers': n_workers,
            'NMatched': n_matched,
            'ProportionMatched': n_matched/n_workers
        })


    # Calculate per location-year father stats
    @staticmethod
    def _location_year_father_stats(location_year: pd.DataFrame) -> pd.Series:
        return pd.Series({
            'MeanNFathers': location_year['NFathers'].mean(),
            'MinNFathers': location_year['NFathers'].min(),
            'MaxNFathers': location_year['NFathers'].max(),
            'MeanProportionMatched': location_year['ProportionMatched'].mean(),
            'MaxProportionMatched': location_year['ProportionMatched'].max(),
            'MinProportionMatched': location_year['ProportionMatched'].min()
        })
    
    
    # Compare match father groups with the correct father groups
    def _father_group_correct(self, worker: pd.Series) -> bool:
        worker_father_group = self.pedigree_KGD.loc[self.pedigree_KGD['IndivID'] == worker['IndivID']].iloc[0]['FatherGroup']
        father_father_group = self.groups_KGD.loc[self.groups_KGD['IndivID'] == worker['BestFatherMatch']].iloc[0]['ParGroup']
        
        return worker_father_group == father_father_group


if __name__ == '__main__':
    par_plot = ParPlot()
    par_plot.log_correct()
    par_plot.check_father_groups()
    par_plot.plot()
    par_plot.father_stats_to_csv()
    par_plot.workers_annotated_to_csv()