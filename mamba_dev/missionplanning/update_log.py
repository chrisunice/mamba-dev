import mamba_ui as mui
from datetime import datetime
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State


def _timestamp():
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")


def _create_line(name: str, value: list | None):
    if value is None:
        text = ''
    else:
        text = [f"\n\t\t{item}" for item in value]

    return f"{name.upper()}:{''.join(text)}\n"


@mui.app.callback(
    Output('output-log', 'value'),
    Input('mission-planning-page-submit-button', 'n_clicks'),
    State('platform-database-dropdown-checklist', 'value'),
    State('air-vehicle-configuration-dropdown-checklist', 'value'),
    State('air-vehicle-sub-configuration-dropdown-checklist', 'value')
)
def update_log(submit_click, platform, av_config, av_sub_config):
    if submit_click is None:
        raise PreventUpdate

    log_message = f">> ({_timestamp()}) STARTING MPF GENERATION...\n" \
                  f">>\t{_create_line('platform', platform)}" \
                  f">>\t{_create_line('air vehicle configuration(s)', av_config)}" \
                  f">>\t{_create_line('air vehicle sub configurations(s)', av_sub_config)}" \

    # TODO need to add the mission info next to output

    return log_message
