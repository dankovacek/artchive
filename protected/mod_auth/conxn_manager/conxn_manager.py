# from sqlalchemy import create_engine, engine_from_config
# from sqlalchemy.orm import sessionmaker
# # from flask_sqlalchemy import declarative_base
# #from sqlalchemy.ext.declarative import declarative_base
# import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# instance_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'protected/')

# Base = declarative_base()

# #engine = create_engine('sqlite:///' + os.path.join(BASE_DIR, 'artchive.db'))
# engine = engine_from_config(os.path.dirname(os.path.join(BASE_DIR, 'config.py')), url='sqlite:///' + BASE_DIR + '/artchive.db')
# Base.metadata.bind = engine

# # create a Session
# DBSession = sessionmaker(bind=engine)

# dbSession = DBSession()

# class SessionManager(object):

#     def __init__(self):
#         self.dbSession = DBSession()
