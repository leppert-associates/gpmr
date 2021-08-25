import pandas as pd


# load csv file to dataframe
# df = pd.read_csv('data/deertrail_lab.csv', parse_dates=['datetime'])
def load_data(path):
    return pd.read_csv(path, parse_dates=['datetime'])


def get_locations(df):
    return df['location'].unique()


def get_parameters(df):
    return df['parameter'].unique()


def get_data(df, location, parameter):
    dfmi = df.set_index(['location', 'parameter', 'datetime']).sort_index()
    dfmic = dfmi.loc[(location, parameter)].reset_index()
    dfmic['value'].fillna(
        value=dfmic['detection_limit']/2, inplace=True)
    dfmic.sort_values(by='datetime', inplace=True)
    return dfmic


def get_description(dfmi):
    return list(dfmi['value'].describe(
    ).reset_index().itertuples(index=False, name=None))


# should use sqlite or postgres,
#
# SELECT DISTINCT location, parameter FROM lab
# SELECT * WHERE location = ? AND parameter = ?
#
