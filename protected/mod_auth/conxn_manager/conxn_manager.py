from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import declarative_base
#from sqlalchemy.ext.declarative import declarative_base
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

Base = declarative_base()
engine = create_engine('sqlite:///' + os.path.join(BASE_DIR, 'artchive.db'))
Base.metadata.bind = engine
#Base.metadata.create_all(engine)

# create a Session
DBSession = sessionmaker(bind=engine)

dbSession = DBSession()

class SessionManager(object):

    def __init__(self):
        self.dbSession = DBSession()
