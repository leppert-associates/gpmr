import pandas as pd


class Data:

    def __init__(self, path: str) -> None:
        # Open connection to database instead
        self.df = pd.read_csv(path, parse_dates=['datetime']).set_index(
            ['location', 'parameter', 'datetime']).sort_values(by='datetime').sort_index()

    @property
    def locations(self):
        # SELECT DISTINCT location FROM lab
        return self.df.index.unique('location')

    @property
    def parameters(self):
        # SELECT DISTINCT parameter FROM lab
        return self.df.index.unique('parameter')

    def fill_na(self):
        self.df['value'].fillna(
            value=self.df['detection_limit']/2, inplace=True)
        return self

    def get_data(self, location, parameter):
        # "SELECT value, datetime, detection_limit
        # WHERE location = ? AND parameter = ?",
        # (location, parameter)
        return self.df.loc[(location, parameter)].reset_index()


def get_description(df):
    return list(df['value'].describe(
    ).reset_index().itertuples(index=False, name=None))
