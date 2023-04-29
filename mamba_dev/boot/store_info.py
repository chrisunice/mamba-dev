import os
import json
from flask import request
from datetime import datetime
from dash_extensions.enrich import Trigger, Output, State

import mamba_ui as mui
from mamba_dev import config


@mui.app.callback(
    Output('session-store', 'data'),
    Trigger('dash-layout', 'children'),
    State('session-store', 'data')
)
def store_session_serverside(session_data):
    """ Store a session folder for the client on the server that is tied to the life of the browser """
    if session_data is None:
        # Make client folder
        root_dir = config['default']['root_dir']
        username = request.authorization['username']
        client_folder = f"{root_dir}/clients/{username}"

        # Make a client folder if one doesn't already exist
        try:
            os.mkdir(client_folder)
        except FileExistsError:
            pass

        # Make a session folder for the client
        dt = datetime.utcnow()
        string_time = dt.strftime("%Y-%m-%d_%H.%M.%SZ")
        session_folder = f"{client_folder}/{string_time}"
        try:
            os.mkdir(session_folder)
        except:
            pass

        return json.dumps(dict(_dummy=None))
    else:
        return session_data
