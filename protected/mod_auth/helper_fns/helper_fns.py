from flask import Flask, session

from functools import wraps

import sys
import os

#sys.path.insert(0, os.path.abspath('..'))

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
INSTANCE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.pardir, os.pardir))

class helperManager(SessionManager):

    def login_required(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'email' in session:
                return f(*args, **kwargs)
            else:
                flash('You do how have access permission')
                return redirect('/login')
        return decorated_function

    def get_key(self, key_file, api_type, descriptor):
        with open(key_file) as api_data_file:
            data = json.load(api_data_file)
            return data[api_type][descriptor]

    def get_api_key(self, service, api_type, descriptor):
        """Retrieves various client secrets"""
        if service == 'oauth2':
            return self.get_key(INSTANCE_DIR + '/client_secrets.json',
                                api_type, descriptor)
        elif service == 'places_search':
            return self.get_key(INSTANCE_DIR + '/api_key.json',
                                api_type, descriptor)
        elif service == 'secret_key':
            return self.get_key(INSTANCE_DIR + '/client_secrets.json',
                                api_type, descriptor)

    def get_current_user(self):
        """Retrieves the current user by email address"""
        try:
            email = session['email']
            user = self.dbSession.query(User).filter_by(email=email).one()
            return user
        except Exception:
            return None

    def get_current_user_id(self):
        """Retrieves the current user by email address"""
        try:
            email = session['email']
            user = self.dbSession.query(User).filter_by(email=email).one()
            return user.id
        except Exception:
            return None

    def create_new_user(self, session_obj):
        # Ensure duplicate users aren't added to the database.
        # Each user must have a unique email address.
        current_user = self.get_current_user()
        if current_user is None:
            # create new user object
            new_user = User()
            new_user.name = session_obj['username']
            new_user.email = session_obj['email']
            new_user.picture = session_obj['picture']
            new_user.provider = session_obj['provider']
            new_user.provider_id = session_obj['provider_id']
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
