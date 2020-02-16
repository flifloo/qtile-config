from libqtile import hook
from subprocess import run


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
    elif c.name in ["Lutris", "Shadow", "Steam"] or c.name[:9] == "Minecraft":
        c.togroup("\N{video game}")


@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    run(["xrandr", "--auto"])
    qtile.cmd_restart()

