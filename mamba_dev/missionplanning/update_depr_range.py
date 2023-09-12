import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import CycleBreakerInput, Output, ctx


@mui.app.callback(
    Output('depression-range-slider', 'value'),
    Output('depression-range-min-input', 'value'),
    Output('depression-range-max-input', 'value'),
    CycleBreakerInput('depression-range-slider', 'value'),
    CycleBreakerInput('depression-range-min-input', 'value'),
    CycleBreakerInput('depression-range-max-input', 'value'),
)
def update_depr_range(
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



