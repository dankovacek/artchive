from flask import Flask, url_for, render_template, request, Blueprint
from flask import redirect, session, make_response, flash, jsonify

from helper_fns.helper_fns import helperManager
from login.login import login_ext
#from modules.database_setup import database_setup
from models.models import User
from conxn_manager.conxn_manager import SessionManager

import cgi
import httplib2
import jinja2
import json
import os
import re
import random
import requests
import string
import sys

# import the db
from app import db
from app import graffikiApp

# create the mod_auth blueprint that gets registered in
# init.py
#mod_auth = Blueprint('auth', __name__, url_prefix='/auth')
app = Blueprint('default', __name__)

# create an instance of helperManager class to access helper functions

class MainAppManager(SessionManager):

    """ Main routing features for app. """

    @app.route('/')
    def Main():
        #currentUser = helpers.get_current_user()
        #items = helpers.get_all_items()
        return render_template('index.html')#, items=items, user=currentUser)

    # # display only the current user's items
    # @app.route('/users/<int:user_id>/')
    # def my_items(user_id):
    #     try:
    #         items = helpers.get_all_user_items(user_id)
    #         return render_template('content.html',
    #                                user=helpers.get_current_user(),
    #                                items=items)
    #     except Exception:
    #         return redirect('/')
    #
    # # delete an item
    # @helpers.login_required
    # @app.route('/delete/<int:user_id>/<int:item_id>/', methods=['GET'])
    # def delete_item(user_id=None, item_id=None):
    #     currentUser = helpers.get_current_user()
    #     if request.method == 'GET':
    #         if user_id is None and item_id is None:
    #             return redirect('/users/' + str(currentUser.id) + '/')
    #         else:
    #             currentItem = helpers.get_single_user_item(user_id, item_id)
    #             if currentUser.id != user_id:
    #                 flash("You don'thave permission to delete this item.")
    #                 return redirect('/login')
    #             else:
    #                 helpers.edit_delete_item(currentItem)
    #                 flash("Item deleted.")
    #                 return redirect('/users/' + str(currentUser.id) + '/')