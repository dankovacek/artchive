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
template_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public/app/templates')
print 'templates ==========>', template_folder
#define the config folder
# d = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

static_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public/app/static')

# Define the WSGI application object
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

# Configurations
# Point the path to the parent directory
app.config.from_object('protected.config')
app.config.from_pyfile('config/config.py')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Configure Secret Key
# (https://github.com/pallets/flask/wiki/Large-app-how-to)
def install_secret_key(app, filename='secret_key'):
    """Configure the SECRET_KEY from a file
    in the protected directory.

    If the file does not exist, print instructions
    to create it from a shell with a random key,
    then exit.
    """
    filename = os.path.join(app.instance_path, filename)

    try:
        app.config['SECRET_KEY'] = open(filename, 'rb').read()
    except IOError:
        print('Error: No secret key. Create it with:')
        full_path = os.path.dirname(filename)
        if not os.path.isdir(full_path):
            print('mkdir -p {filename}'.format(filename=full_path))
        print('head -c 24 /dev/urandom > {filename}'.format(filename=filename))
        sys.exit(1)

if not app.config['DEBUG']:
    install_secret_key(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import module / components using their blueprint handler variable (mod_auth)
from mod_auth.main import app as default_module
from mod_auth.login.login import login_ext

# Register blueprints
app.register_blueprint(default_module)
#graffikiApp.register_blueprint(auth_module)
app.register_blueprint(login_ext)
