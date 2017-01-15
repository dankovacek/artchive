from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import Boolean, DateTime, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker

from mod_auth.conxn_manager.conxn_manager import Base, engine
from mod_auth.conxn_manager.conxn_manager import dbSession
from mod_auth.conxn_manager.conxn_manager import SessionManager

# import os
# import sys

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(80), unique=True, nullable=False)
    picture = Column(String(200), nullable=True)
    provider = Column(String(200))
    provider_id = Column(String(200))
    created = Column(DateTime, default=datetime.utcnow())

    # For printing User objects for debugging
    def __repr__(self):
        return '<User %r>' % (self.name)

Base.metadata.create_all(engine)
