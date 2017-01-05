import os
import sys

from mod_auth.helper_fns.helper_fns import helperManager

# Run a server.
from public import app

# create helperManager instance
helpers = helperManager()

# detects changes and automatically restarts server
app.secret_key = helpers.get_api_key(
    'secret_key', 'web', 'client_secret')
app.debug = True
# app.session_interface = ItsdangerousSessionInterface()
app.run(host='0.0.0.0', port=5000)
