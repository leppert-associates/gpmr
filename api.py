from abc import ABC, abstractmethod
from sqlalchemy import *
from sqlalchemy.orm import Session
import pandas as pd


class Engine(ABC):
    @abstractmethod
    def create_engine(self):
        pass


class SqlachemyEngine(Engine):

    def __init__(self, uri) -> None:
        super().__init__()
        if uri.startswith('postgres://'):
            self.uri = uri.replace('postgres://', 'postgresql://', 1)
        self.uri = uri

    def create_engine(self):
        return create_engine(self.uri)


class Facility():

    def __init__(self, engine: Engine, facility: str, schema: str) -> None:
        self.engine = engine
        self.facility = facility
        self.schema = schema
        if self.schema not in inspect(self.engine).get_schema_names():
            self.engine.execute(schema.CreateSchema(self.schema))
        self.table = Table(self.facility, MetaData(),
                           schema=self.schema, autoload_with=self.engine)

    def get_fields(self):
        return self.table.columns.keys()

    def get_locations(self):
        stmt = select(self.table.c.location).distinct().order_by(
            self.table.c.location)
        with Session(self.engine) as session:
            return session.execute(stmt)

    def get_parameters(self):
        stmt = select(self.table.c.parameter).distinct().order_by(
            self.table.c.parameter)
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

    def csv_to_db(self, csv_file: str):
        '''FIXME: need to check if data exists in table '''
        df = pd.read_csv(csv_file, parse_dates=['datetime']).sort_values(
            by='datetime', inplace=True)
        df.to_sql(self.facility,
                  con=self.engine,
                  schema=self.schema,
                  if_exists='append',
                  index=False)
