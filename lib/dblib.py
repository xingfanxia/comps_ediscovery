'''
Database library for interacting with sqlite/pandas dataframes
'''
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.pool import StaticPool

class Database():
    def __init__(self):
        self.conn = sqlalchemy.create_engine('sqlite:///../data/parsed/databases/ediscovery.db', connect_args={'check_same_thread':False}, poolclass=StaticPool)
        self.metadata = MetaData(self.conn)
        Session = sessionmaker(bind=self.conn)
        self.session = Session()
        self.emails = Table('emails', self.metadata, autoload=True)

    '''
    Writes a table of a given name to the database from a passed in dataframe
    '''
    def df_to_table(self, df, tablename):
        df = df[df.columns[~df.columns.str.contains('Unnamed:')]]
        df.to_sql(tablename, self.conn, if_exists="replace", index=False)

    '''
    For parts of our project that only need to READ our database,
    but never write anything, this will pull the current state of the
    database into a pd dataframe for it to read from.
    '''
    def df_from_table(self, tablename):
        return pd.read_sql_table(tablename, self.conn)

    '''
    Returns a full email row based on its ID
    '''
    def get_email_by_id(self, id, scenario=None):
        print(id)
        res = self.session.query(self.emails).filter_by(ID=id)
        if scenario:
            res = res.filter_by(Scenario=str(scenario))
        res = res.all()
        return [r._asdict() for r in res]

    #only returning 5000 results rn
    def get_scenario(self, scenario):
        res = self.session.query(self.emails).filter_by(Scenario=str(scenario)).limit(5000).all()
        return [r._asdict() for r in res]
