import os
import sys

from mod_auth.helper_fns.helper_fns import helperManager

from public import app

# create helperManager instance
helpers = helperManager()

# app.session_interface = ItsdangerousSessionInterface()
app.run(host='0.0.0.0', port=5000)
