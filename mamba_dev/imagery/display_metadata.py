import pandas as pd
from dash.dependencies import Input, Output, State

import mamba_ui as mui


@mui.app.callback(
    Output('carousel-caption', 'children'),
    Input('imagery-carousel', 'active_index'),
    State('imagery-store', 'data'),
    State('carousel-caption', 'children')
)
def display_caption(active_index, data, existing_children):
    if active_index is None:
        return existing_children

    df = pd.DataFrame.from_records(data, index='index')

    return df.ImagePath[active_index]
