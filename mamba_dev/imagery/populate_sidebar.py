import lodat as lo
from dash.dependencies import Input, Output

import mamba_ui as mui


@mui.app.callback(
    Output('platform-dropdown', 'options'),
    Output('band-dropdown', 'options'),
    Output('polarization-dropdown', 'options'),
    Input('sql-database-dropdown', 'value'),
    prevent_initial_call=True
)
def populate_sidebar(_):
    dbm = lo.ImageryDatabaseManager()
    platforms = dbm.platforms
    bands = dbm.bands
    pols = dbm.polarizations
    dbm.close()
    return platforms, bands, pols
