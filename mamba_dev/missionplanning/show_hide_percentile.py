import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State, ctx


@mui.app.callback(
    Output('percentile-row', 'style'),
    Input('mission-planning-page', 'children'),
    Input('compute-metric-dropdown-checklist', 'value'),
    State('percentile-row', 'style')
)
def show_hide_percentile(_, checklist_value, row_style):
    if ctx.triggered_id is None or checklist_value is None:
        raise PreventUpdate

    if ctx.triggered_id == 'mission-planning-page':
        row_style['display'] = 'none'
    elif ctx.triggered_id == 'compute-metric-dropdown-checklist':
        if checklist_value[0].lower() == 'percentile':
            row_style['display'] = 'flex'
        else:
            row_style['display'] = 'none'
    return row_style
