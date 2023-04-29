import os
from flask import request
from dash_extensions.enrich import Trigger

import mamba_ui as mui
from mamba_dev import config


@mui.app.callback(
    Trigger('dash-layout', 'children')
)
def store_serverside():
    # Make client folder
    root_dir = config['default']['root_dir']
    username = request.authorization['username']
    client_folder = f"{root_dir}/clients/{username}"

    try:
        os.mkdir(client_folder)
    except FileExistsError:
        pass
    