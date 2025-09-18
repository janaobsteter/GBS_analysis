import pandas as pd
from plotnine import *
from matplotlib import colormaps
from matplotlib.colors import to_hex
import numpy as np

# Add colony UID column to deepforest patrilines file (looked up in MS data file)
def add_colony_uid(colony: pd.Series) -> pd.Series:
    colony['colony_uid'] = MS.loc[MS['queen'] == colony['queen']].iloc[0]['colony_uid']
    return colony

# Add microlocation_colony_uid column to patrilines
def add_microlocation_colony_uid(colony: pd.Series) -> pd.Series:
    microlocation = MS.loc[MS['colony_uid'] == colony['colony_uid']].iloc[0]['microlocation']
    colony['microlocation_colony_uid'] = str(int(microlocation)) + ' ' + str(int(colony['colony_uid']))
    
    return colony

# Load CSVs
patrilines_vrata_2022 = pd.read_excel('./MS/vrata-2022_MS_patrilines.xlsx')
patrilines_vrata_2023 = pd.read_excel('./MS/vrata-2023_MS_patrilines.xlsx')
patrilines_deepforest_2022 = pd.read_excel('./MS/deepforest-2022_MS_patrilines.xlsx')

MS = pd.read_csv('./MS/MS.csv')

# Prepare and concat
patrilines_deepforest_2022 = patrilines_deepforest_2022.apply(add_colony_uid, axis=1)

patrilines_vrata_2022['Location-Year'] = 'vrata-2022'
patrilines_vrata_2023['Location-Year'] = 'vrata-2023'
patrilines_deepforest_2022['Location-Year'] = 'deepforest-2022'

patrilines = pd.concat([patrilines_vrata_2022, patrilines_vrata_2023, patrilines_deepforest_2022])

# Add microlocation info for plotting
patrilines = patrilines.apply(add_microlocation_colony_uid, axis=1)

# Get colormap
viridis = colormaps['viridis']

# Plot each location-year combination separately
for location_year in patrilines['Location-Year'].unique():
    # Convert patrilines to long format, so min and max patrilines can be plotted as columns next to one another
    patrilines_long = patrilines[patrilines['Location-Year'] == location_year].melt(
        id_vars='microlocation_colony_uid',
        value_vars=['max_patrilines', 'min_patrilines'],
        var_name='variable',
        value_name='value'
    )
    
    plot = (
        ggplot(patrilines_long) +
        geom_col(aes(
            y='value',
            x='microlocation_colony_uid',
            fill='variable'
            ),
            position='dodge'
        ) +
        theme(
            axis_text_x=element_text(
                angle=90, 
            )
        ) +
        labs(
            y='Number patrilines (estimated from MS data)',
            x='Microlocation and colony UID',
            title=location_year,
        ) +
        scale_fill_manual(
            name='Patrilines',
            labels=['Estimated maximum', 'Estimated minimum'],
            values=[to_hex(viridis(i)) for i in np.linspace(0, 0.8, 2)]
        ) +
        scale_y_continuous(
            breaks=range(0, patrilines_long['value'].max(), 5)
        )
    )
    
    plot.save(filename=f'./plots/{location_year}_MS_patrilines.png')