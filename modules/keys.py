from datetime import datetime
from os import getenv, execl
from pathlib import Path
from subprocess import run, Popen, PIPE

from libqtile.config import Key, Drag, Click
from libqtile.lazy import lazy

from modules import mod


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
    Key([mod, "mod1"], "n", lazy.spawn(f"{exitvenv} kitty --name nvim nvim")),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.toggle_floating()),
]

