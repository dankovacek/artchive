from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from flask import Flask, url_for, render_template, request
from flask import redirect, session, make_response, flash, jsonify

from flask import Blueprint
from protected.mod_auth.helper_fns.helper_fns import helperManager
from protected.mod_auth.conxn_manager.conxn_manager import SessionManager

from protected.mod_auth.models.models import Base, User, dbSession

import cgi
import httplib2
# import hmac
import jinja2
import json
import os
import re
import random
import requests
import string
import sys

# create an instance of helperManager class to access helper functions
helpers = helperManager()

# create the mod_auth blueprint that gets registered in
# __init__.py
static_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public/app/static')
login_ext = Blueprint('login_ext', __name__)

CLIENT_ID = helpers.get_api_key('oauth2', 'web', 'client_id')

APPLICATION_NAME = "artchive"

INSTANCE_DIR = os.path.join(os.path.dirname(__file__),
                            os.pardir, os.pardir, 'instance')


class LoginManager(SessionManager):
    # Login and Authorization
    # Create anti-forgery state token

    @login_ext.route('/login', methods=['GET'])
    def ShowLogin():
        """Render login page if user session doesn't exist.
        Otherwise, redirect to the main page."""
        if request.method == 'GET':
            current_user = helpers.get_current_user()
            if current_user is None:
                state = ''.join(
                    random.choice(
                        string.ascii_uppercase + string.digits)
                    for x in xrange(32))
                session['state'] = state
                return render_template("login.html", STATE=state, user=None)
            else:
                return redirect('/')

    # Facebook Oauth2 login flow
    @login_ext.route('/fbconnect', methods=['GET', 'POST'])
    def FbConnect():
        if request.method == 'GET':
            return request()

        if request.method == 'POST':
            # request.params['state']
            # flask uses request.args.get('...')
            if request.args.get('state', '') != session['state']:
                error(401)
            # retrieve the access token from ajax request body.
            # this comes from the javascript in login.html
            access_token = request.data
            print "access token received %s " % access_token

            app_id = json.loads(
                open(INSTANCE_DIR + '/fb_client_secrets.json', 'r')
                .read())['web']['app_id']
            app_secret = json.loads(
                open(INSTANCE_DIR + '/fb_client_secrets.json', 'r')
                .read())['web']['app_secret']
            url = 'https://graph.facebook.com/oauth/access_token?'
            url += 'grant_type=fb_exchange_token&'
            url += 'client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
                app_id, app_secret, access_token)
            h = httplib2.Http()
            result = h.request(url, 'GET')[1]

            # Use token to get user info from API
            userinfo_url = "https://graph.facebook.com/v2.4/me"
            # strip expire tag from access token
            token = result.split("&")[0]

            url = 'https://graph.facebook.com/v2.4/'
            url += 'me?%s&fields=name,id,email' % token
            h = httplib2.Http()
            result = h.request(url, 'GET')[1]
            print "url sent for API access:%s"% url
            print "API JSON result: %s" % result
            data = json.loads(result)

            session['email'] = data["email"]
            session['provider'] = 'facebook'
            session['username'] = data["name"]
            session['provider_id'] = data["id"]

            # The token must be stored in the login_session in order to properly
            # logout, let's strip out the information before
            # the equals sign in our token
            stored_token = token.split("=")[1]
            session['access_token'] = stored_token

            # Get user picture
            url = 'https://graph.facebook.com/v2.4/me/'
            url += 'picture?%s&redirect=0&height=200&width=200' % token
            h = httplib2.Http()
            result = h.request(url, 'GET')[1]
            data = json.loads(result)

            session['picture'] = data["data"]["url"]
            # self.session['user_ID'] == user.ID
            # print "self.session['user_ID']: %s" % self.session['user_ID']

            # Check if user already exists
            check_user = helpers.get_current_user()
            if check_user is not None:
                return redirect('/')

            new_user = helpers.create_new_user(session)
            output = ''
            output += '<h1>Welcome, '
            output += session['username']

            output += '!</h1>'
            output += '<img src="'
            output += session['picture']
            output += ' " class="welcome-picture">'
            print 'Done!'
            return output

    # Google Oauth2 login flow
    @login_ext.route('/gconnect', methods=['POST'])
    def GConnect():
        if request.method == 'POST':
            # Validate state token
            if request.args.get('state', '') != session['state']:
                response = make_response(json.dumps('State token error.'), 401)
                return response

            # Obtain authorizaton code
            # flask uses request.data for files in the body,
            # (instead of request.body)
            code = request.data
            try:
                # Upgrade the authorization code into a credentials object
                oauth_flow = flow_from_clientsecrets(
                    INSTANCE_DIR + '/client_secrets.json', scope='')
                oauth_flow.redirect_uri = 'postmessage'
                credentials = oauth_flow.step2_exchange(code)
            except FlowExchangeError:
                print 'flowexchangeerror'
                # response.headers['Content-Type'] = 'application/json'
                response = make_response(
                    json.dumps('Failed to upgrade the authorization code.'),
                    401)
                return response

            # Check that the access token is valid.
            access_token = credentials.access_token
            url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
                   % access_token)
            h = httplib2.Http()
            result = json.loads(h.request(url, 'GET')[1])

            # If there was an error in the access token info, abort.
            if result.get('error') is not None:
                print 'flowexchangeerror'
                response = make_response(
                    json.dumps(
                        'There was an error in the access token info.'), 401)
                return response
                # response.set_status(401)
                # response.headers['Content-Type'] = 'application/json'

            # Verify that the access token is used for the intended user.
            gplus_id = credentials.id_token['sub']
            if result['user_id'] != gplus_id:
                response = make_response(
                    json.dumps(
                        "Token's user ID doesn't match given user ID."), 401)
                return response
                # write("Token's user ID doesn't match given user ID.")
                # response.headers['Content-Type'] = 'application/json'

            # Verify that the access token is valid for this app.
            if result['issued_to'] != CLIENT_ID:
                response = make_response(
                    json.dumps("Token's client ID does not match app's."), 401)
                return response
                # write("Token's client ID does not match app's.")
                # response.set_status(401)
                # response.headers['Content-Type'] = 'application/json'

            stored_token = session.get('access_token')
            stored_gplus_id = session.get('gplus_id')

            if stored_token is not None and gplus_id == stored_gplus_id:
                response = make_response(
                    json.dumps("Current user is already connected."), 200)
                return response
                # write('Current user is already connected.')
                # response.set_status(200)
                # response.headers['Content-Type'] = 'application/json'

            # Store the access token in the session for later use.
            session['access_token'] = access_token
            session['provider_id'] = gplus_id

            # Get user info
            userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
            params = {'access_token': credentials.access_token, 'alt': 'json'}
            answer = requests.get(userinfo_url, params=params)
            data = answer.json()

            session['username'] = data['name']

            # If no username is specified (google requires only email)
            if not data['name']:
                email_str_ind = data['email'].index('@')
                session['username'] = data['email'][0:email_str_ind]

            session['picture'] = data['picture']
            session['email'] = data['email']
            # ADD PROVIDER TO LOGIN SESSION
            session['provider'] = 'google'

            # Check if user already exists
            check_user = helpers.get_current_user()
            if check_user is not None:
                return redirect('/')

            new_user = helpers.create_new_user(session)
            output = ''
            output += '<h1>Welcome, '
            output += session['username']
            output += '!</h1>'
            output += '<img src="'
            output += session['picture']
            output += ' " class="welcome-picture">'
            print "done!"
            return output

    # DISCONNECT - Revoke a current user's token and reset their login_session
    def GDisconnect(self):
        # Only disconnect a connected user.
        access_token = session.get('access_token')
        if access_token is None:
            response = make_response(
                json.dumps("Current user not connected."), 401)
            return response
            # self.write("Current user not connected.")
            # response.set_status(401)
            # response.headers['Content-Type'] = 'application/json'
        url = 'https://accounts.google.com/o/oauth2/'
        url += 'revoke?token=%s' % access_token
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]
        if result['status'] != '200':
            # For whatever reason, the given token was invalid.
            response = make_response(\
                json.dumps("Current user not connected."), 400)
            return response
            # self.write("Failed to revoke token for given user.")
            # response.set_status(400)
            # response.headers['Content-Type'] = 'application/json'
        return "you have been logged out"

    def FbDisconnect(self):
        facebook_id = session['provider_id']
        # The access token must me included to successfully logout
        access_token = session.get('access_token')
        url = 'https://graph.facebook.com/'
        url += '%s/permissions?access_token=%s' % (
            facebook_id, access_token)
        try:
            h = httplib2.Http()
            result = h.request(url, 'DELETE')[1]
            if result['status'] != '200':
                # For whatever reason, the given token was invalid.
                response = make_response(\
                    json.dumps("Current user not connected."), 400)
                return response
        except Exception:
            return "There was an issue logging you out.  \
            Check your connection and try again."

    # Route the disconnect function to the appropriate provider disconnect
    # function
    @helpers.login_required
    @login_ext.route('/logout')
    def Disconnect():
        login_mgr = LoginManager()
        if 'provider' in session:
            provider = session['provider']
            if provider == 'google':
                login_mgr.GDisconnect()
            if provider == 'facebook':
                login_mgr.FbDisconnect()
            del session['username']
            del session['provider_id']
            del session['email']
            del session['picture']
            del session['provider']
            del session['access_token']
            print("Logout successful.")
        else:
            print("You were not logged in to begin with.")
        return redirect('/')
