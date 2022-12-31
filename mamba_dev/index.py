import mamba_ui as mui
from mamba_dev import config

# Home page callbacks
from mamba_dev.home.display_page import display_page
from mamba_dev.home.toggle_menubar import toggle_menubar
from mamba_dev.home.store_data import store_uploaded_data
from mamba_dev.home.change_menu_icon import change_menu_icon
from mamba_dev.home.toggle_upload import toggle_upload_window

# Imagery page callbacks
from mamba_dev.imagery.display_images import display_images
from mamba_dev.imagery.display_metadata import display_caption
from mamba_dev.imagery.populate_sidebar import populate_sidebar
from mamba_dev.imagery.show_database_icon import show_database_icon

# Data visualization page callbacks
from mamba_dev.data_vis.populate_data_selector import data_source, vector_group
from mamba_dev.data_vis.render_plot import render_plot
from mamba_dev.data_vis.toggle_databar import toggle_databar
from mamba_dev.data_vis.show_filter_icon import show_filter_icon
from mamba_dev.data_vis.switch_tabs import switch_tabs


if __name__ == "__main__":

    mui.app.layout = mui.serve_layout()

    run_kwargs = dict(
        debug=bool(int(config['default']['debug_mode'])),
        host=config['default']['ip_address'],
        port=int(config['default']['port'])
    )
    if run_kwargs.get('debug'):
        run_kwargs.pop('host')
    mui.app.run(**run_kwargs)
