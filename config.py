from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook

from typing import List  # noqa: F401
from os import getenv, environ, execl
from subprocess import run, Popen

import widget_custom

mod = "mod4"
newpath = getenv("PATH").replace("/opt/qtile/venv/bin", "")
exitvenv = f"env -u VIRTUAL_ENV PATH='{newpath}'"


def cmd_run(prompt, sudo=False):
    name = "cmd"
    if sudo:
        name += "(root)"
    def f(args):
        if sudo:
            args = f"sudo -A {args}"
        Popen(f"{exitvenv} {args}", shell=True)

    prompt.start_input(name, f, "cmd")


def hard_restart(misc):
    execl("/opt/qtile/qtile-venv-entry",  " ")


keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "Tab", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),

    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    # Windows opacity
    Key([mod, "shift"], "o", lazy.window.down_opacity()),
    Key([mod, "shift"], "t", lazy.window.up_opacity()),

    # Qtile managment
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "f", lazy.function(hard_restart)),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod, "control"], "s", lazy.spawn("systemctl poweroff")),
    Key([mod, "control"], "v", lazy.spawn("xtrlock"), lazy.spawn("systemctl suspend")),

    # Run
    Key([mod], "r", lazy.widget["prompt"].function(cmd_run)),
    Key([mod, "shift"], "r", lazy.widget["prompt"].function(cmd_run, True)),
    
    # Lock
    Key([mod], "l", lazy.spawn(f"xtrlock")),
    Key([mod, "control"], "l", lazy.spawn(f"parrots -n 9 -l")),
    Key([mod, "shift"], "l", lazy.spawn(f"xtrlock -b")),

    # Brightness
    Key(["mod1"], "F7", lazy.spawn("xbrightness 0.5")),
    Key(["mod1"], "F6", lazy.spawn("xbrightness +0.2")),
    Key(["mod1"], "F5", lazy.spawn("xbrightness -0.2")),

    # Audio
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 -D default -q set Master 2%+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 -D default -q set Master 2%-")),
    Key([], "XF86AudioMute", lazy.spawn("amixer -c 0 -D default -q set Master toggle")),

    # Apps
    Key([mod, "mod1"], "k", lazy.spawn(f"{exitvenv} kitty")),
    Key([mod, "mod1"], "v", lazy.spawn(f"{exitvenv} vivaldi")),
    Key([mod, "mod1"], "d", lazy.spawn(f"{exitvenv} discord")),
    Key([mod, "mod1"], "t", lazy.spawn(f"{exitvenv} telegram-desktop")),


    # Notify
    Key([mod, "mod1"], "Right", lazy.widget["notify"].next()),
    Key([mod, "mod1"], "Left", lazy.widget["notify"].prev()),
    Key([mod, "mod1"], "Down", lazy.widget["notify"].clear()),

]


groups = []
for i in [["F1", "\N{globe with meridians}"], ["F2", "\N{incoming envelope}"], ["F3", "\N{briefcase}"], ["F4", "\N{floppy disk}"], ["F5", "\N{bookmark tabs}"], ["F6", "\N{video game}"]]:
    groups.append(Group(i[1]))
    keys.extend([
        Key([mod], i[0], lazy.group[i[1]].toscreen()),
        Key([mod, "shift"], i[0], lazy.window.togroup(i[1], switch_group=True))
        ])


layouts = [
    layout.Max(),
    layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    #layout.Columns(),
    #layout.Matrix(),
    #layout.MonadTall(),
    #layout.MonadWide(),
    #layout.RatioTile(),
    #layout.Tile()
    #layout.TreeTab(),
    #layout.VerticalTile(),
    #layout.Zoomy(),
]


widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(),
                widget.GroupBox(hide_unused=True),
                widget.Prompt(),
                widget.TaskList(txt_floating="🗗", txt_maximized="🗖", txt_minimized="🗕"),
                widget.Systray(),
                widget.Notify(),
                widget.CheckUpdates(custom_command="apt list --upgradable", execute="sudo -A apt update", display_format="{updates}", colour_have_updates="ff7300", colour_no_updates="5eff00"),
                widget.Sep(),
                widget.CPU(format="{load_percent}%"),
                widget_custom.Memory(),
                widget.ThermalSensor(tag_sensor="Core 0"),
                widget.Sep(),
                widget.Wlan(disconnected_message="", interface="wlp1s0"),
                widget.Net(format="{down}\u2193\u2191{up}"),
                widget.Sep(),
                #widget.BatteryIcon(battery="BATC"),
                widget.Battery(charge_char="\N{electric plug}", discharge_char="\N{battery}", empty_char="\N{cross mark}", unknown_char="\N{question mark}", battery="BATC", format="{char}{percent:2.0%} {hour:d}:{min:02d}", low_percentage=0.35, hide_threshold=True),
                widget.Volume(front="material-design-icons-iconfont",emoji=True),
                widget.Clock(format='%d/%m/%Y %H:%M'),
            ],
            24,
        ),
    ),
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]


dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = True
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wname': 'Onboard'},
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])

auto_fullscreen = True
focus_on_window_activation = "smart"


@hook.subscribe.client_new
def func(c):
    if c.name == "Vivaldi - Vivaldi":
        c.togroup("\N{globe with meridians}")
    elif c.name in ["Discord", "Telegram"]:
        c.togroup("\N{incoming envelope}")
    elif c.name == "Typora":
        c.togroup("\N{briefcase}")
    elif c.name == "win0":
        c.togroup("\N{floppy disk}")
    elif c.name == "docs":
        c.togroup("\N{bookmark tabs}")
    elif c.name in ["Lutris", "Shadow"]:
        c.togroup("\N{video game}")


def main(q):
    Popen(["nextcloud", "--background"])
    Popen("kdeconnect-indicator")

wmname = "LG3D"

