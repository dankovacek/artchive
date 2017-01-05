from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import Boolean, DateTime, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker

from mod_auth.conxn_manager.conxn_manager import Base, engine, dbSession
from mod_auth.conxn_manager.conxn_manager import SessionManager

import os
import sys

sys.path.insert(0, os.path.abspath('..'))

class User(Base):
    __tablename__ = 'auth_user'
    extend_existing = True
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(80), unique=True, nullable=False)
    provider = Column(String(200))
    provider_id = Column(String(200))
    created = Column(DateTime, default=datetime.utcnow())

    def __init__(self, name, email):

        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)

# Base.metadata.create_all(engine)
