import textwrap
import pyodbc
import pandas as pd


def db_connect(db_path: str, driver='{Microsoft Access Driver (*.mdb, *.accdb)}') -> str:
    conn_str = (
        f"DRIVER={driver};"
        f"DBQ={db_path};"
    )
    conn = pyodbc.connect(conn_str)
    sql = textwrap.dedent("""
    SELECT
    p.CASNumber, p.ParameterName,
    r.Value, u.UnitName, r.DetectionLimit, r.DilutionFactor, r.MDL, r.Method, r.SampleNumber,
    l.Location,
    c.CollectionTime, c.Laboratory
    FROM ((((AnalyteResult AS r
        LEFT OUTER JOIN Unit AS u
            ON u.UnitID = r.UnitID)
        LEFT OUTER JOIN AnalyteParameter AS p
            ON p.AnalyteParameterID = r.AnalyteParameterID)
        LEFT OUTER JOIN AnalyteCollect AS c
            ON c.AnalyteCollectID = r.AnalyteCollectID)
        LEFT OUTER JOIN Location AS l
            ON l.LocationID = c.LocationID)
    """)
    df = pd.DataFrame(pd.read_sql_query(sql, conn))
    conn.close()
    return df


def scrub_df(df):
    # Format dataframe, sort by date
    df.rename(columns={'CollectionTime': 'Time',
              'ParameterName': 'Parameter', 'UnitName': 'Unit', 'CASNumber': 'CAS'}, inplace=True)
    df['Time'] = pd.to_datetime(df['Time'])
    df.sort_values('Time', inplace=True)
    df.reset_index(inplace=True, drop=True)
    # Remove null value placeholders:
    # ND Value as '-99.0'
    df.loc[df['Value'] < 0, 'Value'] = None
    df.loc[df['DetectionLimit'] < 0, 'DetectionLimit'] = None
    df.loc[df['MDL'] < 0, 'MDL'] = None
    # Method as 'Unknown', 'UNK' or 'Unk'
    df.loc[df['Method'] == 'Unknown', 'Method'] = None
    df.loc[df['Method'] == 'UNK', 'Method'] = None
    df.loc[df['Method'] == 'Unk', 'Method'] = None
    # Laboratory as 'Unknown Laboratory'
    df.loc[df['Laboratory'] == 'Unknown Laboratory', 'Laboratory'] = None
    df.loc[df['Laboratory'] == 'Unknown', 'Laboratory'] = None
    # SampleNumber
    df.loc[df['SampleNumber'] == 'Unknown', 'SampleNumber'] = None
    return df


# # Print to csv
# df = db_connect(
#     r'C:\Users\iaxelrad\Documents\GitHub\ECIMS\db\DeerTrail.accdb')
# clean_df = scrub_df(df)
# clean_df.to_csv('deertrail.csv', index=False)
