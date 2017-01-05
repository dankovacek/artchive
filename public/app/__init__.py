# changed setting in /usr/local/lib/python2.7/dist-packages/
# flask_sqlalchemy/__init__.py:800
# track_modifications =
# app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
# was originally None, but changed to suppress warning.

# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

import os
import sys

# define the templates folder
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

#define the config folder
d = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
config_folder = os.path.join(d, 'protected/config')

# Define the WSGI application object
app = Flask(__name__, template_folder=template_folder)

# Configurations
# Point the path to the parent directory
# from protected import config
# app.config.from_object(config)
#print config, '&&&&&&&&&&&&&&&'
# print "asdfaaaaaaa ", config.DEBUG
app.config.from_pyfile(os.path.join(config_folder, 'config.py'))
# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import module / components using their blueprint handler variable (mod_auth)
#from main import mod_auth as auth_module
from protected.mod_auth.main import app as default_module
from mod_auth.login.login import login_ext

# Register blueprints
app.register_blueprint(default_module)
#graffikiApp.register_blueprint(auth_module)
app.register_blueprint(login_ext)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
