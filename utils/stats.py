import numpy as np
import scipy
import pymannkendall as mk


# The `Population` class contains the queried data from a particular parameter at a specific location
class Population:
    alpha = 0.05
    max_deviations = 2

    def __init__(self, data) -> None:
        self.data = data

    def log(self):
        self.data['Value'] = np.log(self.data['Value'])
        return self

    def censor(self):
        self.data.dropna(subset=['Value'])
        return self

    def count_nd(self):
        self.count = self.data.shape[0]
        self.hits = self.data['Value'].count()
        self.nd = self.data['Value'].isnull().sum()
        self.percent_nd = (self.nd/self.count)*100

    def reject_outliers(self):
        d = np.abs(self.data['Value'] - np.median(self.data['Value']))
        m_dev = np.median(d)
        s = d/m_dev if m_dev else 0.
        self.data = self.data[s < self.max_deviations]
        return self

    # returns: statistic, p-value
    def shapiro(self):
        return scipy.stats.shapiro(self.data['Value'])

    # Mann-Kendall test. Returns: trend, h, p, z, Tau, s, var_s, slope (sens?), intercept
    def mk_test(self):
        return mk.original_test(self.data['Value'], self.alpha)

    def get_sum_stats(self):
        # Pandas describe()
        [self.count, self.mean, self.std, self.min, self.first_q,
            self.median, self.third_q, self.max] = self.data['Value'].describe()
        # SciPy describe() - count, min, max, & mean overlap w/ pd!
        [self.nobs, self.minmax, self.mean, self.skewness, self.kurtosis, self.variation] = scipy.stats.describe(
            self.data['Value'])
        # self.data['Value'].describe()
        return scipy.stats.describe(self.data['Value'])
