import pandas as pd


# Import and clean data, should be postgres
def get_data():
    return pd.read_csv(r'data/deertrail.csv', parse_dates=['datetime'])
