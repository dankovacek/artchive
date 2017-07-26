# changed setting in /usr/local/lib/python2.7/dist-packages/
# flask_sqlalchemy/__init__.py:800
# track_modifications =
# app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
# was originally None, but changed to suppress warning.

import cgi
import os
import sys
import jinja2
import json
import os
import re
import random
import requests
import string
import sys

# Import flask
from flask import Flask, url_for, render_template, request, Blueprint
from flask import redirect, session, make_response, flash, jsonify
from flask import send_from_directory

from sqlalchemy.orm import sessionmaker

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
#import flask_wtf
#from wtforms import Form, TextField, validators

from mod_auth.helper_fns.helper_fns import helperManager
from mod_auth.models.models import SessionManager

# Import all models before the db.create_all() function is executed
from mod_auth.models.models import User

# create an instance of helperManager class to access helper functions
helpers = helperManager()


#######################
# changed setting in /usr/local/lib/python2.7/dist-packages/
# flask_sqlalchemy/__init__.py:800
# track_modifications =
# app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
# was originally None, but changed to suppress warning.

# Import flask
from flask import Flask

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Import main and login python files as separate modules
# and register them so routing can occur from separate files
from mod_auth.login.login import login_ext
from mod_auth.main import main_app

# Import all models before the db.create_all() function is executed
from mod_auth.models.models import User

import os
import sys

# define the templates folder
# template_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public/app/templates')

# static_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public/app/static')

instance_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'protected/')

# Define the WSGI application object
app = Flask(__name__)

# Configurations
# Point the path to the parent directory
#app.config.from_object('config')
app.config.from_pyfile(os.path.join(instance_path, 'config/config.py'))

# Register the Blueprint sub-components for main and login
app.register_blueprint(login_ext, url_prefix='/login_ext/')#, template_folder=app.config.get('TEMPLATE_DIR'))
#app.register_blueprint(main_app, template_folder=app.config.get('TEMPLATE_DIR'))

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
    filename = os.path.join(app.config.get('INSTANCE_PATH'), filename)

    try:
        app.config['SECRET_KEY'] = open(filename, 'rb').read()
    except IOError:
        print('Error: No secret key. Create it with:')
        full_path = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir(full_path):
            print('mkdir -p {filename}'.format(filename=full_path))
        print('head -c 24 /dev/urandom > {filename}'.format(filename=filename))
        sys.exit(1)

if not app.config['DEBUG']:
    install_secret_key(app)


class MainAppManager(SessionManager):
    """ Main routing features for app. """
    @main_app.route('/')
    def index():
        """Check if user is logged in.  If not, set state token
        for login flow."""
        currentUser = helpers.get_current_user()
        if currentUser:
            items = None #helpers.get_all_items()
            #state = None
            return render_template('index.html', user=currentUser)
        else:
            return redirect('/login')
    #     #, items=items, user=currentUser)

    @helpers.login_required
    @app.route('/flickr_key_query', methods=["GET"])
    def flickr_key_query():
        # Get Flickr API Key
        api_key = helpers.get_api_key('flickr', 'flickr', 'api_key')
        return jsonify(result=api_key)

    @helpers.login_required
    @app.route('/geolocate_key_query', methods=["GET"])
    def geolocate_key_query():
        """Routing for Google Maps API key retrieval."""
        api_key = helpers.get_api_key('places_search', 'maps', 'api_key')
        return jsonify(result=api_key)

    # Sample HTTP error handling
    @app.errorhandler(404)
    def not_found(error):
        return render_template(url_for('app.templates', filename='404.html'), 404)

    # Handler for letsencrypt?
    @app.route('/.well-known/acme-challenge/<path:filename>')
    def send_challenge(filename):
        return send_from_directory(app.config['WELL_KNOWN_DIR'], filename)






