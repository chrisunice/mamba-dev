import os
import dash_auth

import mamba_ui as mui
from mamba_dev import config
from mamba_dev import logger

from mamba_dev.boot import *
from mamba_dev.home import *
from mamba_dev.settings import *
from mamba_dev.sandbox import *
from mamba_dev.missionplanning import *


if __name__ == "__main__":

    logger.debug(f'Parent: ({os.getppid()}) - Starting mamba...')

    # App Authentication
    dash_auth.BasicAuth(
        app=mui.app,
        username_password_list={dct['username']: dct['password'] for idx, dct in config.get('users').items()}
    )

    # Connect the layout
    mui.app.layout = mui.serve_layout()

    # Launch the server
    if config.get('server_debug_mode'):
        run_kwargs = config['run_modes']['development']
    else:
        run_kwargs = config['run_modes']['production']
    mui.app.run(**run_kwargs)

