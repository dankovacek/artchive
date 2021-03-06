from flask import Flask, url_for, render_template, request, Blueprint
from flask import redirect, session, make_response, flash, jsonify

from helper_fns.helper_fns import helperManager
from models.models import User
from conxn_manager.conxn_manager import SessionManager

import cgi
#import httplib2
import jinja2
import json
import os
import re
import random
import requests
import string
import sys

# create the mod_auth blueprint that gets registered in
# init.py
# mod_auth = Blueprint('auth', __name__, url_prefix='/auth')
main_app = Blueprint('main_app', __name__)

# create an instance of helperManager class to access helper functions
helpers = helperManager()

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
    @main_app.route('/flickr_key_query', methods=["GET"])
    def flickr_key_query():
        # Get Flickr API Key
        api_key = helpers.get_api_key('flickr', 'flickr', 'api_key')
        return jsonify(result=api_key)

    @helpers.login_required
    @main_app.route('/geolocate_key_query', methods=["GET"])
    def geolocate_key_query():
        """Routing for Google Maps API key retrieval."""
        api_key = helpers.get_api_key('places_search', 'maps', 'api_key')
        return jsonify(result=api_key)

    # Sample HTTP error handling
    @main_app.errorhandler(404)
    def not_found(error):
        return render_template(url_for('templates', filename='404.html'), 404)

    # # display only the current user's items
    # @app.route('/users/<int:user_id>/<name>')
    # def my_items(user_id, username):
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
