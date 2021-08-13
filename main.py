import pandas as pd
import matplotlib.pyplot as plt


# Create plots using lists of locations and parameters
def plot_figs(df, locs, params):
    dfmi = df.set_index(['Location', 'Parameter', 'Time'],
                        append=False).sort_index()
    for loc in locs:
        for param in params:
            fig = plt.figure(figsize=(10, 7.5))
            ax = fig.add_subplot(111)
            for p in params[param]:
                sub_df = dfmi.loc[(loc, p)].reset_index(level='Time')
                sub_df.plot(x='Time', y='Value', kind='line',
                            logy=True, grid=True, subplots=False, marker='o', label=p, title=f"{loc} {param}", ax=ax)
            ax.set_ylabel(f"Concentration ({sub_df.Unit[0]})")
            ax.legend(loc='center left', frameon=False,
                      bbox_to_anchor=(1, 0.5))
            plt.tight_layout()
            fig.savefig(f"output/{loc}_{param}", orientation='landscape')
            plt.clf()
            plt.close('all')


# Put in postgres db...
# Facility wide 'raw' data
df = pd.read_csv(r'data/deertrail.csv', parse_dates=['Time'], engine='python')

# # Multi-Index dataframe
multi = df.set_index(['Location', 'Parameter', 'Time']).sort_index()


# Should be table in db that is brought in as multi-index
locs = ['L3-42']  # df['Location'].unique()
cas = {"Metals": ['7439-89-6', '7439-92-1', '7439-96-5', '7439-97-6', '7440-02-0', '7440-22-4',
                  '7440-23-5', '7440-38-2', '7440-43-9', '7440-47-3', '7440-66-6', '7740-39-3', '7782-49-2']}
params = {"Inorganic": ['ARSENIC (DISSOLVED)', 'Arsenic (TOTAL)', 'Chloride', 'Fluoride',
                        'Nitrogen, Nitrate-Nitrite', 'Organic Carbon, Total', 'Sulfate', 'Zinc (TOTAL)']}


# need to check if we get a hit for every analyte in the permit
# should really just add a column for analyte group to db
plot_figs(df, locs, params)
