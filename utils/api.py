import pandas as pd


# load csv file to dataframe
df = pd.read_csv(r'data/deertrail_lab.csv', parse_dates=['datetime'])


def get_locations(df=df):
    return df['location'].unique()


def get_parameters(df=df):
    return df['parameter'].unique()


def get_data(location, parameter, df=df):
    dfmi = df.set_index(['location', 'parameter', 'datetime']).sort_index()
    dfmic = dfmi.loc[(location, parameter)].reset_index()
    dfmic['value'].fillna(
        value=dfmic['detection_limit']/2, inplace=True)
    dfmic.sort_values(by='datetime', inplace=True)
    # get sum stats
    desc_list = list(dfmic['value'].describe(
    ).reset_index().itertuples(index=False, name=None))

    return dfmic, desc_list


# should use sqlite, and write api
#
# SELECT DISTINCT location, parameter FROM lab
# SELECT * WHERE location = ? AND parameter = ?
#
