import pyodbc
import pandas as pd

# conn_str = (
#     r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
#     r"DBQ=C:\Users\iaxelrad\Documents\GitHub\ECIMS\db\ECIMS.accdb;"
# )
# conn = pyodbc.connect(conn_str)
# sql = "SELECT Analyte, CAS FROM Analyte"
# df = pd.DataFrame(pd.read_sql_query(sql, conn))
# df.to_csv('analytes.csv', index=False)
# conn.close()


df = pd.read_csv(r'data/analytes.csv')
df.sort_values('CAS', inplace=True)
df.reset_index(inplace=True, drop=True)
df.to_csv('analytes2.csv', index=False)
