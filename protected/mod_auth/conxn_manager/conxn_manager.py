from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import declarative_base
#from sqlalchemy.ext.declarative import declarative_base
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

Base = declarative_base()
engine = create_engine('sqlite:///' + os.path.join(BASE_DIR, 'graffikiApp.db'))
Base.metadata.bind = engine
#Base.metadata.create_all(engine)

# create a Session
DBSession = sessionmaker(bind=engine)

dbSession = DBSession()

class SessionManager(object):

    def __init__(self):
        self.dbSession = DBSession()

# I need to develop a generalized approach to backend setup
# including server configuration, security, basic app launch,
# testing, and production tools / tasks.
