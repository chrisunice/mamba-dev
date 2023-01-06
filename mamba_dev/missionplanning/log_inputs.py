import os
from datetime import datetime
import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State

from mamba_dev import config


@mui.app.callback(
    Output('mission-planning-placeholder', 'children'),
    Input('mission-planning-page-submit-button', 'n_clicks'),
    [
        State('platform-database-dropdown-checklist', 'value'),
        State('air-vehicle-configuration-dropdown-checklist', 'value'),
        State('air-vehicle-sub-configuration-dropdown-checklist', 'value'),
        State('missions-dropdown-checklist', 'value'),
        State('vector-groups-dropdown-checklist', 'value'),
        State('look-range-min-input', 'value'),
        State('look-range-max-input', 'value'),
        State('depression-range-min-input', 'value'),
        State('depression-range-max-input', 'value'),
        State('look-bin-width', 'value'),
        State('depression-bin-width', 'value'),
        State('minimum-hits/bin', 'value'),
        State('minimum-missions/bin', 'value'),
        State('compute-metric-dropdown-checklist', 'value'),
        State('percentile', 'value')
    ]
)
def log_inputs(
        submit_click: int,
        platform: list,
        av_config: list,
        av_sub_config: list,
        missions: list,
        vectors: list,
        look_min: int,
        look_max: int,
        depr_min: int,
        depr_max: int,
        look_width: int,
        depr_width: int,
        hits_per_bin: int,
        msn_per_bin: int,
        metric: list,
        percentile: int
):
    # Do nothing until the submit button is clicked
    if submit_click is None:
        raise PreventUpdate

    # Make log folder
    log_path = f"{config['default']['root_dir']}\\logs\\missionplanning.log"
    if not os.path.exists(os.path.dirname(log_path)):
        os.makedirs(os.path.dirname(log_path))

    # Helper functions
    timestamp = lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def fmt_arg(x: list | None):
        if not isinstance(x, list):
            return x
        else:
            try:
                x.remove('Select all')
            except ValueError:
                pass
            return ', '.join(x)

    # Add to log file
    with open(log_path, mode='w+') as log:
        log.write(f'{timestamp()} - Platform: {fmt_arg(platform)}\n')
        log.write(f'{timestamp()} - Air Vehicle Configuration: {fmt_arg(av_config)}\n')
        log.write(f'{timestamp()} - Air Vehicle Sub Configuration: {fmt_arg(av_sub_config)}\n')
        log.write(f'{timestamp()} - Missions: {fmt_arg(missions)}\n')
        log.write(f'{timestamp()} - Vectors: {fmt_arg(vectors)}\n')
        log.write(f'{timestamp()} - Look Range: [{look_min}, {look_max}]\n')
        log.write(f'{timestamp()} - Depression Range: [{depr_min}, {depr_max}]\n')
        log.write(f'{timestamp()} - Bin Size: [{look_width}, {depr_width}]\n')
        log.write(f'{timestamp()} - Minimum Hits/Bin: {hits_per_bin}\n')
        log.write(f'{timestamp()} - Minimum Missions/Bin: {msn_per_bin}\n')
        metric_msg = metric if percentile is None else f"{fmt_arg(metric)} (P{percentile})"
        log.write(f'{timestamp()} - Compute Metric: {metric_msg}\n')

    return None
