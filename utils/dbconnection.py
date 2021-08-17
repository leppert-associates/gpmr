import pyodbc
import psycopg2
import pandas as pd
import sqlalchemy as sa
import psutil


# move to .env file...
server = 'leppert-sql-server.database.windows.net'
database = 'ECIMS'
username = 'leppert'
password = 'Rockies1422'

#self._localServer = 'localhost'
# localServer = '192.168.3.114'
# localDatabase = 'ECIMS_Local'
# localUsername = 'postgres'

# DbConnection(server, database, username, password)


class DbConnection():
    def __init__(self, server, database, username, password, port='5432', driver='{ODBC Driver 17 for SQL Server}'):
        self._server = server
        self._database = database
        self._username = username
        self._password = password
        self._driver = driver
        self._port = port

    def connect_cloud(self):
        self._connection_string = f"DRIVER={self._driver};SERVER='{self._server}';DATABASE='{self._database}';UID='{self._username}';PWD='{self._password}'"
        self._connection = pyodbc.connect(self._connection_string)
        self._cursor = self._connection.cursor()
        # What's this?
        self._connection_URL = sa.engine.url.URL(
            "mssql+pyodbc", query={"odbc_connect": self._connection_string})
        self._engine = sa.create_engine(self._connection_URL)

    def connect_local(self):
        self._connection = psycopg2.connect(host=self._server,
                                            port=self._port,
                                            database=self._database,
                                            user=self._username,
                                            password=self._password)

        self._cursor = self._connection.cursor()
        self._engine = sa.create_engine(
            f"postgresql://{self._username}:{self._password}@{self._server}/{self._database}")

    def Close(self):
        self._connection.close()
        del self._connection
        del self._cursor
        del self._engine

    # ##########################################################################
    # # Check schema size to ensure available RAM is large enough for download - else return False
    # def MemoryCheck(self, facility_id):
    #     available_GB = psutil.virtual_memory().available / (1024.0 ** 3)
    #     sizes = pd.DataFrame(pd.read_sql_query("SELECT SCHEMA_NAME(so.schema_id) AS SchemaName "
    #                                            "    , SUM(ps.reserved_page_count) * 8.0 / 1024 AS SizeInMB "
    #                                            "FROM sys.dm_db_partition_stats ps "
    #                                            "JOIN sys.indexes i "
    #                                            "ON i.object_id = ps.object_id "
    #                                            "AND i.index_id = ps.index_id "
    #                                            "    JOIN sys.objects so "
    #                                            "    ON i.object_id = so.object_id "
    #                                            "WHERE so.type = 'U' "
    #                                            "GROUP BY so.schema_id "
    #                                            "ORDER BY OBJECT_SCHEMA_NAME(so.schema_id), SizeInMB DESC;", self._connection))

    #     if facility_id in sizes["SchemaName"].tolist():
    #         needed_GB = sizes.loc[sizes["SchemaName"]
    #                               == str(facility_id), "SizeInMB"].item()

    #         if float(needed_GB) <= (0.5 * available_GB):
    #             return True

    #         else:
    #             return False

    #     else:
    #         return False

    # # Function for select queries - pull records from existing table
    # def Select(self, query):
    #     result = pd.DataFrame(pd.read_sql_query(
    #         query, self._connection, coerce_float=True))
    #     return result

    # # Grab a table

    # def GetTable(self, tableName, tableSchema):
    #     result = self.Select("SELECT * FROM \"" +
    #                          tableSchema + "\"." + tableName + ";")
    #     return result

    # # Pull all data from Admin database (No facility data)
    # def GetAdmin(self, schema_id):
    #     Tables = {}

    #     # if self.MemoryCheck('0'):
    #     Tables_Info = pd.DataFrame(pd.read_sql_query(("SELECT table_name "
    #                                                   + "FROM information_schema.tables "
    #                                                   + "WHERE table_schema = \'"
    #                                                   + schema_id + "\' AND "
    #                                                   + "table_type='BASE TABLE';"),
    #                                                  self._connection,
    #                                                  params=[schema_id]))
    #     Table_Names = Tables_Info["table_name"].tolist()

    #     # Loop through table names - retrieve all in admin schema
    #     for name in Table_Names:
    #         Tables[str(name)] = self.GetTable(name, schema_id)

    #     return Tables

    # # Pull all data from one facility schema
    # def GetFacility(self, facility_id):
    #     Tables = {}

    #     # if self.MemoryCheck(facility_id):
    #     Tables_Info = pd.DataFrame(pd.read_sql_query("SELECT T.name, S.id "
    #                                                  "FROM sys.tables AS T "
    #                                                  "LEFT OUTER JOIN sys.schemas AS S "
    #                                                  "  ON S.[schema_id] = T.[schema_id] "
    #                                                  "WHERE S.[name] LIKE '" + str(facility_id) + "';", self._connection))

    #     # Possible that facility schema / id does not yet exist so dataframe is empty - return tables as 0 length dictionary
    #     if Tables_Info.shape[0] == 0:
    #         return Tables

    #     # Else - populate and return
    #     else:
    #         Table_Names = Tables_Info["name"].tolist()

    #         for name in Table_Names:
    #             Tables[str(name)] = self.GetTable(name, facility_id)

    #     return Tables

    # # Function for insert statements - add new records to a table

    # def Insert(self, table, schema, df):
    #     # write the DataFrame to a table in the sql database
    #     # Arguments include table name (str), schema name (str), and dataframe of entries to append.
    #     # Dataframe must include entry in every row for primary and foreign id's
    #     df.to_sql(table,
    #               con=self._engine,
    #               schema=schema,
    #               if_exists='append',
    #               index=False)

    #     return
