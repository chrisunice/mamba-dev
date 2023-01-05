from dash_extensions.enrich import Output, Input

import mamba_ui as mui


@mui.app.callback(
    Output('menu-icon', 'className'),
    Input('menubar', 'is_open')
)
def change_menu_icon(is_open):
    if is_open:
        return 'fa-solid fa-xmark fa-2xl'
    else:
        return 'fa-solid fa-bars fa-2xl'
