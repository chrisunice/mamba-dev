from dash_extensions.enrich import Trigger, Output

import mamba_ui as mui


# def disable_tab_focus():
#     return clientside_callback(
#         """
#         function disableTabFocus(i) {
#             const handles = document.getElementsByClassName('rc-slider-handle');
#             for (let i = 0; i < handles.length; i++) {
#                 handles[i].setAttribute('tabindex', '-1');
#                 }
#         }
#
#         // Call the function when the app starts
#         disableTabFocus();
#         console.log('I made it');
#         """,
#         Input('mission-planning-page', 'children')
#     )

@mui.app.callback(
    Output('look-range-slider', 'tabindex'),
    Output('depression-range-slider', 'tabindex'),
    Trigger('mission-planning-page', 'children')
)
def disable_tab_index():
    print('disable tab index')
    return -1, -1
