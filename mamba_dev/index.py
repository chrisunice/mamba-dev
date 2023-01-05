import mamba_ui as mui
from mamba_dev import config

# Callbacks
from mamba_dev.home import *
from mamba_dev.datavis import *
from mamba_dev.imagery import *
from mamba_dev.missionplanning import *


if __name__ == "__main__":

    mui.app.layout = mui.serve_layout()

    run_kwargs = dict(
        debug=bool(int(config['default']['debug_mode'])),
        host=config['default']['ip_address'],
        port=int(config['default']['port'])
    )
    if run_kwargs.get('debug'):
        run_kwargs.pop('host')
    mui.app.run(**run_kwargs)
