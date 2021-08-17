import pandas as pd
from db import db_connect, db_field
from scrub import scrub_df
from plot_cvt import plot_cvt


# Print to csv from db
def db_to_csv(path):
    df = db_connect(path)
    df.to_csv('data/deertrail_raw.csv', index=False)
    clean_df = scrub_df(df)
    clean_df.to_csv('data/deertrail.csv', index=False)


# Get facility wide 'raw' data and plot
def plot_me():
    df = pd.read_csv(r'data/deertrail.csv', parse_dates=['DateTime'])
    wells = ['L3-42']
    params = {'Inorganic': ['Arsenic (Dissolved)', 'Arsenic (Total)', 'Chloride', 'Fluoride',
                            'Nitrogen, Nitrate-Nitrite', 'Organic Carbon, Total', 'Sulfate', 'Zinc (Total)']}
    # need to check if we get a hit for every analyte in the permit
    flat_list = [j for sub in [*params.values()] for j in sub]
    if(all(p in df['Parameter'].unique() for p in flat_list)):
        plot_cvt(df, params, wells)
    else:
        print('Missing parameters')


# plot_me()
# db_to_csv(r'C:\Users\iaxelrad\Documents\GitHub\gpmr\data\DeerTrail.accdb')
df = db_field(r'C:\Users\iaxelrad\Documents\GitHub\gpmr\data\DeerTrail.accdb')
df.to_csv('data/field.csv', index=False)
