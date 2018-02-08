'''
Database library for interacting with sqlite/pandas dataframes
'''
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, and_
from sqlalchemy.orm import mapper, sessionmaker, Query
from sqlalchemy.pool import StaticPool
import ast
import datetime

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
        df = df.astype(str)
        df.to_sql(tablename, self.conn, if_exists="replace", index=False)

    '''
    For parts of our project that only need to READ our database,
    but never write anything, this will pull the current state of the
    database into a pd dataframe for it to read from.
    '''
    def df_from_table(self, tablename, scenario=None):
        df = pd.read_sql_table(tablename, self.conn)
        if scenario:
            df = df.loc[df['Scenario'] == str(scenario)]
        df = df.astype(str)
        df['Date'] = pd.to_datetime(df['Date'])
        # df[['To','From','X-To','X-From','Label','Scenario','Relevant','New_Tag']] = df[['To','From','X-To','X-From','Label','Scenario','Relevant','New_Tag']].applymap(ast.literal_eval)
        return df

    '''
    Returns a full email row based on its ID
    '''
    def get_email_by_id(self, id, scenario=None):
        print(id)
        print("here")
        res = self.session.query(self.emails).filter_by(ID=id)
        if scenario:
            res = res.filter_by(Scenario=str(scenario))
        print("here2")
        res = res.all()
        return [r._asdict() for r in res]

    '''
    Gets all emails of a certain scenario
    '''
    #only returning 5000 results rn
    def get_scenario(self, scenario):
        res = self.session.query(self.emails).filter_by(Scenario=str(scenario)).limit(5000).all()
        return [r._asdict() for r in res]

    '''
    Sets an emails relevancy score to either 0 or 1
    '''
    def set_relevancy(self, id, scenario, score):
        stmt = self.emails.update().\
            where(self.emails.c.ID==id).\
            where(self.emails.c.Scenario==str(scenario)).\
            values(Relevant=score)
        self.session.execute(stmt)
        self.session.commit()

    '''
    Gets the tagged emails of a scenario, either goldstandard or user tagged
    for the ML to train off of
    '''
    def get_tagged(self, scenario, goldstandard=False):
        df = self.df_from_table('emails', scenario=scenario)
        df = df.loc[df['New_Tag'] == 1]
        if goldstandard:
            df = df.loc[df['Label'] != -1]
        else:
            df = df.loc[df['Relevant'] != -1]
        stmt = self.emails.update().\
            where(self.emails.c.New_Tag=='1').\
            values(New_Tag='0')
        self.session.execute(stmt)
        self.session.commit()

        return df

    '''
    Gets all untagged emails, either untagged by goldstandard or untagged by user
    of a scenario for the ML to predict off of
    '''
    def get_untagged(self, scenario, goldstandard=False):
        df = self.df_from_table('emails', scenario=scenario)
        if goldstandard:
            df = df.loc[df['Label'] == -1]
        else:
            df = df.loc[df['Relevant'] == -1]
        return df


    '''
    Allows user to query multiple fields and get back all relevant emails
    '''
    def query_helper(self, Date='%', From='%', To='%', Subject='%', Message_Contents='%', ID='%'):
        print('here')
        res = self.session.query(self.emails).filter(and_(self.emails.c.Scenario.contains('401'),
                                                            self.emails.c.Date.contains(Date),
                                                            self.emails.c.From.contains(From),
                                                            self.emails.c.To.contains(To),
                                                            self.emails.c.Subject.contains(Subject),
                                                            self.emails.c.Relevant != ('1'),
                                                            self.emails.c.Relevant != ('0'),
                                                            self.emails.c.Message_Contents.contains(Message_Contents),
                                                            self.emails.c.ID.contains(ID))).all()
        return [r._asdict() for r in res]

    def query(self, dictionary):
        return self.query_helper(**dictionary)

    def reset_new_tag(self):
        stmt = self.emails.update().\
            where(self.emails.c.New_Tag=='1').\
            values(New_Tag='0')
        self.session.execute(stmt)
        self.session.commit()

    def reset_relevant(self):
        stmt = self.emails.update().\
            where(self.emails.c.Relevant != '-1').\
            values(Relevant='-1')
        self.session.execute(stmt)
        self.session.commit()
