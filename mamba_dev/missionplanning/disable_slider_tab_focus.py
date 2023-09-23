import mamba_ui as mui
from dash_extensions.enrich import Trigger


disableTabFocus = mui.app.clientside_callback(
    """
    function disableTabFocus() {
    const handles = document.querySelectorAll('.rc-slider-handle.rc-slider-handle-1, .rc-slider-handle.rc-slider-handle-2');
    for (let i = 0; i < handles.length; i++) {
        handles[i].setAttribute('tabindex', '-1');
        }
    }

    // Call the function when the app starts
    disableTabFocus();
    console.log('I made it');
    """,
    Trigger('mission-planning-page', 'children')
)
