from subprocess import run, PIPE

from libqtile import bar, widget
from libqtile.config import Screen

import widget_custom


widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
screens = []

def main(q):
    ps_screens = int(run("xrandr -q | grep ' connected' | wc -l", shell=True, stdout=PIPE).stdout)
    screens.clear()
    for i in range(ps_screens):
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

