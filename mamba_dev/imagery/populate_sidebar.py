import lodat as lo
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output

import mamba_ui as mui
from mamba_dev import config


@mui.app.callback(
    Output('platform-dropdown', 'options'),
    Output('band-dropdown', 'options'),
    Output('polarization-dropdown', 'options'),
    Input('sql-database-dropdown', 'value'),
)
def populate_sidebar(_):
    if _ is None:
        raise PreventUpdate

    dbm = lo.ImageryDatabaseManager(config['imagery']['imagery_database_path'])
    platforms = dbm.platforms
    bands = dbm.bands
    pols = dbm.polarizations
    dbm.close()
    return platforms, bands, pols
