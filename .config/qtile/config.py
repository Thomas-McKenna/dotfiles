# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import socket
import subprocess
from typing import List  # noqa: F401

from libqtile import bar, hook, layout, widget
from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, Screen

mod = "mod4"

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Move forward or backwards in the group.
    Key([mod, "control"], "l", lazy.screen.next_group()),
    Key([mod, "control"], "h", lazy.screen.prev_group()),

    # increase or decrease master stack horizontal size
    Key([mod],
        "l",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
        desc='Expand window (MonadTall), increase number in master pane (Tile)'
        ),
    Key([mod],
        "h",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
        desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
        ),

    # Stack controls
    Key([mod, "shift"],
        "space",
        lazy.layout.rotate(),
        lazy.layout.flip(),
        desc='Switch which side main pane occupies (XmonadTall)'),

    # cycle through panes
    Key([mod], "space", lazy.layout.next()),
    # launch terminal
    Key([mod], "Return", lazy.spawn("alacritty")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),

    # Kill active window
    Key([mod], "x", lazy.window.kill()),
    # restart Qtile and log out
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.spawn('systemctl suspend')),

    # run command
    Key([mod], "r", lazy.spawncmd()),

    Key([mod], "w", lazy.spawn("firefox"), desc='Start web browser'),
    Key([mod], "e", lazy.spawn("emacs"), desc="Start Emacs"),

    # Switch focus of monitors
    Key([mod], "period", lazy.next_screen(),
        desc='Move focus to next monitor'),
    Key([mod], "comma", lazy.prev_screen(), desc='Move focus to prev monitor'),

    # fullscreen and floating
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc='Toggle Fullscreen'),
    Key([mod], "F", lazy.window.toggle_floating(), desc='Toggle Floating'),
]

# GROUPS #
group_names = [("DEV", {'layout': 'monadtall'}),
               ("CHAT", {'layout': 'max'}),
               ("DOC", {'layout': 'monadtall'}),
               ("MUS", {'layout': 'monadtall'}),
               ("GAME", {'layout': 'max'}),
               ("ETC2", {'layout': 'monadtall'}),
               ("ETC3", {'layout': 'monadtall'}),
               ("VID", {'layout': 'monadtall'}),
               ("WWW", {'layout': 'max'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    # Switch to another group
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))
    # Send current window to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))

# DEFAULT THEME SETTINGS FOR LAYOUTS #####
layout_theme = {
    "border_width": 2,
    "margin": 6,
    "border_focus": "e1acff",
    "border_normal": "1D2330"
}

layouts = [
    # layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
    layout.Floating(**layout_theme)
]

# #### COLOURS ####x#
colours = [
    ["#282a36", "#282a36"],  # panel background
    ["#434758", "#434758"],  # background for current screen tab
    ["#ffffff", "#ffffff"],  # font color for group names
    ["#ff5555", "#ff5555"],  # border line color for current tab
    ["#8d62a9", "#8d62a9"],  # border line color for other tab and odd widgets
    ["#668bd7", "#668bd7"],  # color for the even widgets
    ["#e1acff", "#e1acff"]
]  # window name

# #### PROMPT #####
prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

widget_defaults = dict(font='mononoki Nerd Font',
                       fontsize=16,
                       padding=4,
                       background=colours[1])

extension_defaults = widget_defaults.copy()


# WIDGETS #
def create_widget_list():
    widget_list = [
        widget.GroupBox(font="mononoki Nerd Font",
                        fontsize=18,
                        margin_y=3,
                        margin_x=0,
                        padding_y=5,
                        padding_x=5,
                        borderwidth=3,
                        active=colours[2],
                        inactive=colours[2],
                        rounded=False,
                        highlight_color=colours[5],
                        highlight_method="line",
                        this_current_screen_border=colours[5],
                        this_screen_border=colours[5],
                        other_current_screen_border=colours[0],
                        other_screen_border=colours[0],
                        foreground=colours[2],
                        background=colours[0]),
        widget.Prompt(prompt=prompt,
                      fontsize=18,
                      font="mononoki Nerd Font Bold",
                      foreground=colours[5],
                      background=colours[0]),
        widget.WindowName(foreground=colours[5],
                          background=colours[0],
                          padding=0),
        widget.net.Net(interface="enp7s0",
                       format='{down} ↓↑ {up}',
                       foreground=colours[2],
                       background=colours[5],
                       padding=5),
        widget.CurrentLayoutIcon(
            custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
            foreground=colours[0],
            background=colours[5],
            padding=0,
            scale=0.7),
        widget.CurrentLayout(foreground=colours[2],
                             background=colours[5],
                             padding=5),
        widget.TextBox(text=" Vol:",
                       foreground=colours[2],
                       background=colours[5],
                       padding=0),
        widget.volume.Volume(foreground=colours[2],
                             background=colours[5],
                             padding=5),
        widget.TextBox(text=" 🖬",
                       foreground=colours[2],
                       background=colours[5],
                       padding=0,
                       fontsize=14),
        widget.memory.Memory(foreground=colours[2],
                             background=colours[5],
                             padding=5),
        widget.TextBox(text="Updates: ⟳",
                       padding=2,
                       foreground=colours[2],
                       background=colours[5],
                       fontsize=14),
        widget.pacman.Pacman(execute="alacritty -e sudo pacman -Syu",
                             update_interval=60,
                             foreground=colours[2],
                             background=colours[5]),
        widget.Clock(foreground=colours[2],
                     background=colours[5],
                     format="%A, %B %d  [ %H:%M ]"),
        widget.Systray(background=colours[5], padding=5),
        widget.QuickExit(background=colours[5], default_text="| Shutdown?"),
    ]
    return widget_list


# #### SCREENS ##### (TRIPLE MONITOR SETUP)
shortened_widgets = create_widget_list()
shortened_widgets = [
    shortened_widgets[0], shortened_widgets[2], shortened_widgets[4],
    shortened_widgets[5], shortened_widgets[6], shortened_widgets[7],
    shortened_widgets[12], shortened_widgets[14]
]
screens = [
    Screen(top=bar.Bar(widgets=create_widget_list(), opacity=0.90, size=30)),
    Screen(top=bar.Bar(widgets=shortened_widgets, opacity=0.90, size=30))
]

# Drag floating layouts.
mouse = [
    Drag([mod],
         "Button1",
         lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod],
         "Button3",
         lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {
        'wmclass': 'confirm'
    },
    {
        'wmclass': 'dialog'
    },
    {
        'wmclass': 'download'
    },
    {
        'wmclass': 'error'
    },
    {
        'wmclass': 'file_progress'
    },
    {
        'wmclass': 'notification'
    },
    {
        'wmclass': 'splash'
    },
    {
        'wmclass': 'toolbar'
    },
    {
        'wmclass': 'confirmreset'
    },  # gitk
    {
        'wmclass': 'makebranch'
    },  # gitk
    {
        'wmclass': 'maketag'
    },  # gitk
    {
        'wname': 'branchdialog'
    },  # gitk
    {
        'wname': 'pinentry'
    },  # GPG key password entry
    {
        'wmclass': 'ssh-askpass'
    },  # ssh-askpass
])


# #### STARTUP APPLICATIONS #####
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


@hook.subscribe.startup
def random_wallpapers():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/cycle_pictures.sh'])


@hook.subscribe.client_new
def float_steam(window):
    wm_class = window.window.get_wm_class()
    w_name = window.window.get_name()
    if (wm_class == ("Steam", "Steam") and
        (w_name != "Steam"
         # w_name == "Friends List"
         # or w_name == "Screenshot Uploader"
         # or w_name.startswith("Steam - News")
         or "PMaxSize" in window.window.get_wm_normal_hints().get("flags",
                                                                  ()))):
        window.floating = True


@hook.subscribe.client_new
def float_firefox(window):
    wm_class = window.window.get_wm_class()
    w_name = window.window.get_name()
    if wm_class == ("Places", "firefox") and w_name == "Library":
        window.floating = True


@hook.subscribe.client_new
def float_pycharm(window):
    wm_class = window.window.get_wm_class()
    w_name = window.window.get_name()
    if ((wm_class == ("jetbrains-pycharm-ce", "jetbrains-pycharm-ce")
         and w_name == " ")
            or (wm_class == ("java-lang-Thread", "java-lang-Thread")
                and w_name == "win0")):
        window.floating = True


auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
