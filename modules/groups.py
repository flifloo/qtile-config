from libqtile.config import Group
from libqtile.config import Key
from libqtile.lazy import lazy

from modules import mod
from modules.keys import keys


groups = []
for i in [["F1", "\N{globe with meridians}"], ["F2", "\N{incoming envelope}"], ["F3", "\N{briefcase}"], ["F4", "\N{floppy disk}"], ["F5", "\N{bookmark tabs}"], ["F6", "\N{video game}"]]:
    groups.append(Group(i[1]))
    keys.extend([
        Key([mod], i[0], lazy.group[i[1]].toscreen()),
        Key([mod, "shift"], i[0], lazy.window.togroup(i[1], switch_group=True))
    ])
