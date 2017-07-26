import uuid
import os
import sys

APPLICATION_ROOT = '/'

# Statement for enabling the development environment
# True for development, False for production
DEBUG = False

# Define the application directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))
STATIC_DIR = os.path.join(BASE_DIR, 'public/app/static')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'public/app/templates')
INSTANCE_PATH = os.path.join(BASE_DIR, 'protected/')

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(INSTANCE_PATH, 'artchive.db')
# SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')

DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret12342364524563451345634724563687fsgsy5njnbagakhadkfgjhlajldfhjslhkjljkahhnnbnurahgnvbndhgjsdtyjdhjkhfghtyjukopoiuhgfjnfjymvcnxdfasfwdytifogplfgkhjxfgnxlbkfnlskglhsdfgsfhgdftdfghsg"

SESSION_COOKIE_PATH = os.path.join(BASE_DIR, 'session_cookie')

# API Keys for Google Maps
#GOOGLEMAPS_KEY = ""

SQLALCHEMY_TRACK_MODIFICATIONS = False
