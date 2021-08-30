from abc import ABC, abstractmethod
from sqlalchemy import *
from sqlalchemy.orm import Session
import pandas as pd


class Engine(ABC):
    @abstractmethod
    def create_engine(self):
        pass


class SqlachemyEngine(Engine):

    def __init__(self, connection_uri) -> None:
        super().__init__()
        self.connection_uri = connection_uri

    def create_engine(self):
        return create_engine(
            self.connection_uri,
            echo=True, future=True)


class Facility():

    def __init__(self, engine: Engine, facility: str) -> None:
        self.engine = engine
        self.facility = facility
        self.meta = MetaData()
        self.table = Table(self.facility, self.meta,
                           schema='lab', autoload_with=self.engine)

    def get_fields(self):
        return self.table.columns.keys()

    def get_locations(self):
        stmt = select(self.table.c.location).distinct()
        with Session(self.engine) as session:
            return session.execute(stmt)

    def get_parameters(self):
        stmt = select(self.table.c.parameter).distinct()
        with Session(self.engine) as session:
            return session.execute(stmt)

    def get_parameters_by_location(self, location: str):
        stmt = select(self.table.c.parameter).where(
            self.table.c.location == location).distinct()
        with Session(self.engine) as session:
            return session.execute(stmt)

    def get_values_by_location(self, location: str, parameter: str):
        stmt = select(self.table).where(
            self.table.c.parameter == parameter, self.table.c.location == location)
        with Session(self.engine) as session:
            return session.execute(stmt)


def upload_db(csv_file: str, uri: str):
    '''FIXME: need to check if data exists in table '''
    df = pd.read_csv(csv_file, parse_dates=['datetime']).sort_values(
        by='datetime').sort_index()
    engine = create_engine(uri)
    if not engine.dialect.has_schema(engine, 'lab'):
        engine.execute(schema.CreateSchema('lab'))
    df.to_sql('deertrail',
              con=engine,
              schema='lab',
              if_exists='append',
              index=False)