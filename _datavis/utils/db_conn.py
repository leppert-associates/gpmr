import os
import textwrap
import sqlalchemy
from sqlalchemy import text
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def db_connect(username: str, password: str, server: str, port: int, database: str, query: str):
    ''' Connect to db and execute query. Returns result of query '''
    connection_uri = f"postgresql://{username}:{password}@{server}:{port}/{database}"
    engine = sqlalchemy.create_engine(connection_uri, echo=True, future=True)
    with engine.connect() as conn:
        result = conn.execute(text(query))
    conn.close()
    return result


def clean_db(result):
    ''' Clean the incoming data, return df '''
    df = pd.DataFrame(result)
    # DetectionLimit
    df.columns = ['cas', 'analyte', 'result',
                  'unit', 'qualifier', 'sample', 'datetime']
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.sort_values('datetime', inplace=True)
    df.reset_index(inplace=True, drop=True)
    df.to_csv('data/db_new.csv', index=False)
    return df


def main():
    username = os.getenv('POSTGRES_USERNAME')
    password = os.getenv('POSTGRES_PASSWORD')
    server = os.getenv('POSTGRES_SERVER')
    port = os.getenv('POSTGRES_PORT')
    database = os.getenv('POSTGRES_DATABASE')

    query = textwrap.dedent("""
        SELECT
        a.cas, a.analytename,
        d.dataresults, u.luparameterdescription, d.qualifiers,
        c.fieldsamplenameassignment,
        l.locationarrivaldatetime
        FROM (((("1".samplelabdata d
            LEFT OUTER JOIN "0".analyte a
                ON a.analyteid = d.analyteid)
            LEFT OUTER JOIN "0".ludictionary u
                ON u.ludictionaryid = d.dataresultsunitstypeluid)
            LEFT OUTER JOIN "1".samplecontainer c
                ON c.samplecontainerid = d.samplecontainerid)
            LEFT OUTER JOIN "1".sampledatacollect l
                ON l.sampledatacollectid = c.sampledatacollectid)
    """)

    result = db_connect(username, password,
                        server, port, database, query)
    df = clean_db(result)
    print(df)


if __name__ == "__main__":
    main()
