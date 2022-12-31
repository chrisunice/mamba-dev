import os
import json
from dash import dcc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

import lodat as lo
import mamba_ui as mui

checklist_style = {
    'display': 'flex',
    'flex-direction': 'column',
}

input_style = {
    'margin-right': '10px'
}


@mui.app.callback(
    Output('data-selector-source', 'children'),
    Input('filter-icon', 'n_clicks'),
    State('session-store', 'data'),
    State('data-selector-source', 'children'),
)
def data_source(filter_click, data, original_content):
    # Modular to see if databar has been opened
    databar_is_open = (filter_click % 2 != 0)

    # Databar is open and data has been uploaded
    if databar_is_open and data is not None:
        data = json.loads(data)

        # Build options for checklist
        options = []
        for file in data.get('files'):
            full_path = f"{data.get('upload_dir')}\\{file}"
            file_name = os.path.splitext(file)[0]
            options.append(dict(label=file_name, value=full_path))

        # Return a checklist component
        return dcc.Checklist(id='file-checklist',
                             options=options,
                             inline=False,
                             style=checklist_style,
                             inputStyle=input_style,
                             persistence=True,
                             persistence_type='session')
    else:
        # Otherwise return the default component
        return original_content


@mui.app.callback(
    Output('data-selector-freq', 'children'),
    Output('data-selector-pol', 'children'),
    Output('data-selector-depr', 'children'),
    Input('file-checklist', 'value')
)
def vector_group(sources):
    # Once a data source has been checked
    no_sources = not bool(sources)
    if sources is None or no_sources:
        raise PreventUpdate

    freqs = []
    pols = []
    deprs = []
    for source in sources:
        obj = lo.DataObject(source)
        freqs += obj.frequencies
        pols += obj.polarizations
        deprs.append((obj.raw_data.Depression.min().round(), obj.raw_data.Depression.max().round()))

    freqs = list(map(float, set(freqs)))
    freqs.sort()
    options = [dict(label=f"{freq} MHz", value=f"{freq:.1f}") for freq in freqs]
    freq_checklist = dcc.Checklist(
        id='freq-checklist',
        options=options,
        style=checklist_style,
        inputStyle=input_style,
        persistence=True,
        persistence_type='session'
    )

    pol_checklist = dcc.Checklist(
        id='pol-checklist',
        options=list(set(pols)),
        style=checklist_style,
        inputStyle=input_style
    )

    # Min and max depression are determined by where common depressions exist
    depr_slider = dcc.RangeSlider(
        id='depr-slider',
        min=max([tup[0] for tup in deprs]),
        max=min([tup[1] for tup in deprs]),
        step=1,
        tooltip={'placement': 'left', 'always_visible': True},
        vertical=True
    )
    return freq_checklist, pol_checklist, depr_slider
