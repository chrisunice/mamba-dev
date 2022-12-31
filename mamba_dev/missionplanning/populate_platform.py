import os
import glob
import mamba_ui as mui
from dash.dependencies import Input, Output

from mamba_dev import config


@mui.app.callback(
    Output('platform-database', 'options'),
    Input('mission-planning-page', 'children')
)
def populate_platform(_):
    database_directory = config['test']['test_assets_folder']
    databases = glob.glob(f"{database_directory}\\*mongodb.json")
    return [os.path.basename(db).rstrip('-mongodb.json').upper() for db in databases]
