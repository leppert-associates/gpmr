import pandas as pd
import matplotlib.pyplot as plt


def plot_cvt(df, params, wells=None):
    ''' Create plots using lists of locations and parameters '''
    dfmi = df.set_index(['location', 'parameter', 'datetime']).sort_index()
    if not wells:
        wells = df['Location'].unique()
    for well in wells:
        for param in params:
            fig = plt.figure(figsize=(11, 8.5))
            ax = fig.add_subplot(111)
            for a in params[param]:
                sub_df = dfmi.loc[(well, a)].reset_index()
                sub_df['value'].fillna(
                    value=sub_df['detection_limit']/2, inplace=True)
                sub_df.plot(x='datetime', y='value', logy=True, grid=True,
                            subplots=False, marker='o', label=a,
                            title=f"{well} {param}", ax=ax)
            ax.set_xlabel('Date')
            ax.set_ylabel(f"Concentration ({sub_df.unit[0]})")
            ax.legend(loc='center left', frameon=False,
                      bbox_to_anchor=(1, 0.5))
            plt.tight_layout()
            fig.savefig(f"output/{well}_{param}", orientation='landscape')
            plt.close('all')


if __name__ == "__main__":
    plot_cvt()
