import os
import glob
from dash.dependencies import Input, Output

import mamba_ui as mui


@mui.app.callback(
    Output('platform-database', 'options'),
    Input('mission-planning-page', 'children')
)
def populate_platform(_):
    database_directory = 'C:\\Mamba\\test_assets'
    databases = glob.glob(f"{database_directory}\\*mongodb.json")
    return [os.path.basename(db).rstrip('-mongodb.json').upper() for db in databases]
