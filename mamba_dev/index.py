# Note these are for debugging the processes
import os
import psutil

# from waitress import serve
import dash_auth

import mamba_ui as mui

from mamba_dev import config

from mamba_dev.boot import *
from mamba_dev.home import *
from mamba_dev.settings import *

from mamba_dev.sandbox import *
from mamba_dev.missionplanning import *


if __name__ == "__main__":

    current_pid = os.getpid()
    parent_pid = psutil.Process(current_pid).ppid()
    print(f"The Dash application is running in process: {current_pid} and its parent process is: {parent_pid}")

    # App Authentication
    dash_auth.BasicAuth(
        app=mui.app,
        username_password_list=dict(config['login'])
    )

    mui.app.layout = mui.serve_layout()
    run_kwargs = dict(
        debug=bool(int(config['default']['debug_mode'])),
        host=config['default']['ip_address'],
        port=int(config['default']['port']),
    )
    if run_kwargs.get('debug'):
        run_kwargs.pop('host')
    mui.app.run(**run_kwargs)
