from flask import Flask, session

from functools import wraps

import sys
import os

from protected.mod_auth.models.models import User
from protected.mod_auth.conxn_manager.conxn_manager import dbSession, Base
from protected.mod_auth.conxn_manager.conxn_manager import SessionManager


import random
import string
#import httplib2
import json
import cgi
import os
import re
import requests
import hashlib
import hmac
import jinja2

# create the path to the instance folder for accessing files
INSTANCE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

INSTANCE_DIR += '/api_keys'

class helperManager(SessionManager):

    def login_required(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'email' in session:
                return f(*args, **kwargs)
            else:
                flash('You do not have access permission')
                return redirect('/login')
        return decorated_function

    def get_key(self, key_file, api_type, descriptor):
        with open(key_file) as api_data_file:
            data = json.load(api_data_file)
            api_data_file.closed
            return data[api_type][descriptor]

    def get_api_key(self, service, api_type, descriptor):
        """Retrieves various client secrets"""
        if service == 'oauth2':
            return self.get_key(INSTANCE_DIR + '/client_secrets.json',
                                api_type, descriptor)
        elif service == 'places_search' or service == 'flickr':
            return self.get_key(INSTANCE_DIR + '/api_key.json',
                                api_type, descriptor)
        elif service == 'secret_key':
            return self.get_key(INSTANCE_DIR + '/client_secrets.json',
                                api_type, descriptor)
        elif service == 'fb_client_id':
            return self.get_key(INSTANCE_DIR + '/fb_client_secrets.json',
                                api_type, descriptor)
        elif service == 'fb_secret_key':
            return self.get_key(INSTANCE_DIR + '/fb_client_secrets.json',
                                api_type, descriptor)

    def get_current_user(self):
        """Retrieves the current user by email stored in the session variable address and returns user object"""
        try:
            email = session['email']
            user = self.dbSession.query(User).filter_by(email=email).one()
            return user
        except Exception:
            return None

    def get_user_by_email(self, email):
        """Retrieves User object from db with email address as input."""
        try:
            user = self.dbSession.query(User).filter_by(email=email).one()
            return user
        except Exception:
            return None

    def get_current_user_id(self):
        """Retrieves the current user by email address and returns user id"""
        try:
            email = session['email']
            user = self.dbSession.query(User).filter_by(email=email).one()
            return user.id
        except Exception:
            return None

    def check_if_user_exists(self, email):
        """Checks to see if a user is already registered."""
        try:
            user = self.dbSession.query(User).filter_by(email=email).one()
            return user.email
        except Exception:
            return None

    def create_new_user(self, data):
        # Ensure duplicate users aren't added to the database.
        # Each user must have a unique email address.
        if self.check_if_user_exists(data['email']) is None:
            # create new user object
            new_user = User()
            print data
            new_user.name = data['name']
            new_user.email = data['email']
            new_user.picture = data['picture']
            # Store the provider of Oauth2 login
            new_user.provider = data['provider']
            new_user.provider_id = data['provider_id']
            # add new_user to session staging area and commit
            self.dbSession.add(new_user)
            self.dbSession.commit()
            return "New user added!"
        else:
            return "User already exists."

    def get_all_items(self):
        return self.dbSession.query(Item).all()

    def get_all_user_items(self, user_id):
        return self.dbSession.query(Item)\
            .filter_by(user_id=user_id).order_by('name').all()

    def get_all_items_by_category(self, category_id):
        return self.dbSession.query(Item)\
            .filter_by(category_id=category_id).all()

    def get_single_user_item(self, user_id, item_id):
        return self.dbSession.query(Item)\
            .filter_by(user_id=user_id, id=item_id).one()

    def get_categories(self):
        return self.dbSession.query(Category).order_by('name').all()

    def check_item_category(self, category_name):
        try:
            category = self.dbSession.query(Category)\
                .filter_by(name=category_name).one()
            return category
        except Exception:
            return None

    def create_new_category(self, category_name):
        newCategory = Category()
        newCategory.name = category_name
        self.dbSession.add(newCategory)
        self.dbSession.commit()
        return self.dbSession.query(Category)\
            .filter_by(name=category_name).one()

    def create_item_object(self):
        return Item()

    def add_item(self, currentItem):
        self.dbSession.add(currentItem)
        self.dbSession.commit()
        return

    def edit_delete_item(self, currentItem):
        self.dbSession.delete(currentItem)
        self.dbSession.commit()
        return
