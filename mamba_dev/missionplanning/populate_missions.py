import json
import glob
import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output

from mamba_dev import config


@mui.app.callback(
    Output('missions', 'options'),
    Input('platform-database', 'value'),
)
def populate_missions(platform):
    """ The missions available for a given platform """
    if platform is None:
        raise PreventUpdate

    # Load the database
    path_to_database = glob.glob(f"{config['test']['test_assets_folder']}\\*{platform}*.json")[0]
    with open(path_to_database, mode='r') as f:
        missions = json.load(f)

    # Get UMIs
    umis = [val['umi'] for _, val in missions.items()]
    umis.sort()
    return umis
