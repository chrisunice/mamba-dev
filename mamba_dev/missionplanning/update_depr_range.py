import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import CycleBreakerInput, Output, ctx, State


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


# @mui.app.callback(
#     Output('depression-range-slider', 'value'),
#     Output('depression-range-min-input', 'value'),
#     CycleBreakerInput('depression-range-slider', 'value'),
#     CycleBreakerInput('depression-range-min-input', 'value'),
#     State('depression-range-slider', 'value'),
#     prevent_initial_call=True
# )
# def update_min_depr(slider_value, min_value, old_slider_value):
#     # Do nothing on page load
#     if all([param is None for param in locals().values()]):
#         raise PreventUpdate
#
#     if 'input' in ctx.triggered_id:
#         # Input was triggered
#         if old_slider_value is None:
#             old_slider_value = [None, None]
#         slider_value = [min_value, old_slider_value[-1]]
#     else:
#         # Slider was triggered
#         min_value = slider_value[0]
#     return slider_value, min_value
#
#
# @mui.app.callback(
#     Output('depression-range-slider', 'value'),
#     Output('depression-range-max-input', 'value'),
#     CycleBreakerInput('depression-range-slider', 'value'),
#     CycleBreakerInput('depression-range-max-input', 'value'),
#     State('depression-range-slider', 'value'),
#     prevent_initial_call=True
# )
# def update_max_depr(slider_value, max_value, old_slider_value):
#     # Do nothing on page load
#     if all([param is None for param in locals().values()]):
#         raise PreventUpdate
#
#     if 'input' in ctx.triggered_id:
#         # Input was triggered
#         slider_value = [old_slider_value[0], max_value]
#     else:
#         # Slider was triggered
#         max_value = slider_value[-1]
#     return slider_value, max_value
