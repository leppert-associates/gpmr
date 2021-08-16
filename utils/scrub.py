import re
import pandas as pd


# cleans the incoming data
def scrub_df(df):
    # Format dataframe, sort by date
    # CAS,Parameter,Value,Unit,DetectionLimit,DilutionFactor,MDL,Method,SampleNumber,DataQualifier,Time,Laboratory,Location
    # df.rename(columns={'CASNumber': 'CAS', 'ParameterName': 'Parameter',
    #           'UnitName': 'Unit', 'CollectionTime': 'DateTime'}, inplace=True)
    df.columns = ['cas', 'parameter', 'value', 'unit', 'detection_limit', 'dilution_factor',
                  'mdl', 'method', 'sample_number', 'qualifier', 'datetime', 'laboratory', 'location']
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.sort_values('datetime', inplace=True)
    df.reset_index(inplace=True, drop=True)
    # Remove leading and trailing whitespace
    df['cas'] = df['cas'].str.strip()
    # ND Value as '-99.0' to None
    df.loc[df['value'] < 0, 'value'] = None
    df.loc[(df['value'].isna() & (df['qualifier'].isna())),
           ['qualifier']] = "ND"
    df.loc[df['detection_limit'] < 0, 'detection_limit'] = None
    df.loc[df['mdl'] < 0, 'mdl'] = None
    # Method as 'Unknown', 'UNK' or 'Unk'
    df.loc[df['method'].str.contains(
        r'Unk|Unknown', flags=re.IGNORECASE), 'method'] = None
    # Laboratory as 'Unknown Laboratory'
    df.loc[df['laboratory'].str.contains(
        r'Unknown Laboratory|Unknown', na=False, flags=re.IGNORECASE), 'laboratory'] = None
    # SampleNumber
    df.loc[df['sample_number'].str.contains(
        r'Unknown', na=False, flags=re.IGNORECASE), 'sample_number'] = None
    # Title case if upper
    df.loc[(df['parameter'].str.isupper()) & (df['parameter'].str.contains(r' \(', na=False)),
           'parameter'] = df['parameter'].str.title()
    df.loc[(df['method'].str.isupper()) & (df['method'].str.contains(r'field', na=False, flags=re.IGNORECASE)),
           'method'] = df['method'].str.title()
    # ', Total' to ' (Total)'
    df.loc[(df['parameter'].str.contains(r', Total', flags=re.IGNORECASE)), ['parameter']] = df['parameter'].str.replace(
        r', Total', r' (Total)', flags=re.IGNORECASE)
    # ', Dissolved' to '(Dissolved)'
    df.loc[(df['parameter'].str.contains(r', Dissolved', flags=re.IGNORECASE)), ['parameter']] = df['parameter'].str.replace(
        r', Dissolved', r' (Dissolved)', flags=re.IGNORECASE)
    # Move field in parameter name to method if empty
    df.loc[(df['parameter'].str.contains(r', Field', na=False, flags=re.IGNORECASE))
           & (df['method'].isna()), ['method']] = "Field"
    df.loc[(df['parameter'].str.contains(r', Field', na=False, flags=re.IGNORECASE)), ['parameter']] = df['parameter'].str.replace(
        r', Field', r'', flags=re.IGNORECASE)
    return df
