import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Output, ctx, CycleBreakerInput


@mui.app.callback(
    Output('look-range-slider', 'value'),
    Output('look-range-min-input', 'value'),
    Output('look-range-max-input', 'value'),
    CycleBreakerInput('look-range-slider', 'value'),
    CycleBreakerInput('look-range-min-input', 'value'),
    CycleBreakerInput('look-range-max-input', 'value'),
)
def update_look_range(
        slider_value: tuple[int | float, int | float],
        min_value: int | float,
        max_value: int | float
):
    if all([param is None for param in locals().values()]):
        raise PreventUpdate

    if 'input' in ctx.triggered_id:
        slider_value = [min_value, max_value]
    else:
        # Slider was triggered
        min_value, max_value = slider_value
    return slider_value, min_value, max_value



