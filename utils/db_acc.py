import pyodbc
import pandas as pd


def db_connect(db_path: str, driver='{Microsoft Access Driver (*.mdb, *.accdb)}') -> str:
    conn_str = (
        f"DRIVER={driver};"
        f"DBQ={db_path};"
    )
    conn = pyodbc.connect(conn_str)
    sql = """
    SELECT
    p.CASNumber, p.ParameterName,
    r.Value, u.UnitName, r.DetectionLimit, r.DilutionFactor, r.MDL, r.Method, r.SampleNumber, r.DataQualifier,
    c.CollectionTime, c.Laboratory,
    l.Location
    FROM ((((AnalyteResult AS r
        LEFT OUTER JOIN Unit AS u
            ON u.UnitID = r.UnitID)
        LEFT OUTER JOIN AnalyteParameter AS p
            ON p.AnalyteParameterID = r.AnalyteParameterID)
        LEFT OUTER JOIN AnalyteCollect AS c
            ON c.AnalyteCollectID = r.AnalyteCollectID)
        LEFT OUTER JOIN Location AS l
            ON l.LocationID = c.LocationID)
    """
    df = pd.DataFrame(pd.read_sql_query(sql, conn))
    conn.close()
    return df


# try and get field results as well, add in field params from other df
def db_field(db_path: str, driver='{Microsoft Access Driver (*.mdb, *.accdb)}') -> str:
    conn_str = (
        f"DRIVER={driver};"
        f"DBQ={db_path};"
    )
    conn = pyodbc.connect(conn_str)
    sql = """
    SELECT
    r.CollectionTime, r.Value,
    p.ParameterName,
    u.UnitName,
    l.Location
    FROM (((FieldResult AS r
        LEFT OUTER JOIN Unit AS u
            ON u.UnitID = r.UnitID)
        LEFT OUTER JOIN FieldParameter AS p
            ON p.FieldParameterID = r.FieldParameterID)
        LEFT OUTER JOIN Location AS l
            ON l.LocationID = r.LocationID)
    """
    df = pd.DataFrame(pd.read_sql_query(sql, conn))
    conn.close()
    return df
