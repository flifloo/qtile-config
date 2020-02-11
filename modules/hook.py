from libqtile import hook


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
