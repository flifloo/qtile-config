from libqtile import layout


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
