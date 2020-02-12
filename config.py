from typing import List

from modules.groups import groups
from modules import hook
from modules.keys import keys
from modules.layouts import layouts, floating_layout
from modules.main import main, screens, widget_defaults


groups = groups
keys = keys
layouts = layouts
floating_layout = floating_layout
main = main
screens = screens
extension_defaults = widget_defaults.copy()

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
wmname = "LG3D"

