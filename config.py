from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook

from typing import List  # noqa: F401
from os import getenv, environ, execl
from subprocess import run, Popen, PIPE, STDOUT
from pathlib import Path
from datetime import datetime

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


def screenshot(save=True, copy=True):
    def f(qtile):
        path = Path.home() / "Nextcloud" / "Images" / "Screenshots"
        date = datetime.now()
        path /= f"Screenshot {date.strftime('%d-%m-%Y %H:%S')}.png"
        shot = run(["maim"], stdout=PIPE)

        if save:
            with open(path, "wb") as sc:
                sc.write(shot.stdout)

        if copy:
            run(["xclip", "-selection", "clipboard", "-t",
                            "image/png"], input=shot.stdout)
    return f



def hard_restart(misc):
    execl("/opt/qtile/bin/qtile",  " ")


keys = [
    # Switch between windows in current stack pane
    Key([mod], "Left", lazy.layout.down()),
    Key([mod], "Right", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "control"], "Left", lazy.layout.shuffle_down()),
    Key([mod, "control"], "Right", lazy.layout.shuffle_up()),

    # Move windows to another stack
    Key([mod, "shift"], "Left", lazy.layout.client_to_previous()),
    Key([mod, "shift"], "Right", lazy.layout.client_to_next()),
    
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

    # Screenshots
    Key([], "Print", lazy.function(screenshot())),
    Key(["control"], "Print", lazy.function(save=False)),
    Key(["shift"], "Print", lazy.function(screenshot(copy=False))),

    # Apps
    Key([mod, "mod1"], "k", lazy.spawn(f"{exitvenv} kitty")),
    Key([mod, "mod1"], "v", lazy.spawn(f"{exitvenv} vivaldi")),
    Key([mod, "mod1"], "d", lazy.spawn(f"{exitvenv} discord")),
    Key([mod, "mod1"], "t", lazy.spawn(f"{exitvenv} telegram-desktop")),
    Key([mod, "mod1"], "r", lazy.spawn(f"{exitvenv} kitty --name ranger ranger")),
    Key([mod, "mod1"], "h", lazy.spawn(f"{exitvenv} kitty --name htop htop")),
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
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()
screens = []

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.toggle_floating()),
]


dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {"wmclass": "confirm"},
    {"wmclass": "dialog"},
    {"wmclass": "download"},
    {"wmclass": "error"},
    {"wmclass": "file_progress"},
    {"wmclass": "notification"},
    {"wmclass": "splash"},
    {"wmclass": "toolbar"},
    {"wmclass": "confirmreset"},  # gitk
    {"wmclass": "makebranch"},  # gitk
    {"wmclass": "maketag"},  # gitk
    {"wname": "branchdialog"},  # gitk
    {"wname": "pinentry"},  # GPG key password entry
    {"wname": "Onboard"},
    {"wname": "win0"},
    {"wmclass": "ssh-askpass"},  # ssh-askpass
])

auto_fullscreen = True
focus_on_window_activation = "smart"


@hook.subscribe.client_new
def auto_group(c):
    if c.name == "Vivaldi - Vivaldi":
        c.togroup("\N{globe with meridians}")
    elif c.name in ["Discord", "Telegram"]:
        c.togroup("\N{incoming envelope}")
    elif c.name == "Typora":
        c.togroup("\N{briefcase}")
    elif c.name in ["win0", "DataGrip", "CLion", "IntelliJ IDEA", "PyCharm"]:
        c.togroup("\N{floppy disk}")
    elif c.name == "docs":
        c.togroup("\N{bookmark tabs}")
    elif c.name in ["Lutris", "Shadow"]:
        c.togroup("\N{video game}")


@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    qtile.cmd_restart()


def main(q):
    ps_screens = int(run("xrandr -q | grep ' connected' | wc -l", shell=True, stdout=PIPE).stdout)
    screens.clear()
    for i in range(ps_screens):
        print(1)
        screens.append(Screen(
    top=bar.Bar(
        [
            widget.CurrentLayoutIcon(),
            widget.GroupBox(hide_unused=True),
            widget.Prompt(),
            widget.TaskList(txt_floating="🗗", txt_maximized="🗖", txt_minimized="🗕"),
            widget.Systray(),
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
            widget.Clock(format="%d/%m/%Y %H:%M"),
        ],
        24,
    )
))
 
wmname = "LG3D"

