from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import subprocess
import colors

def get_ip_address():
    # Check if tun0 interface is up
    tun0_check = subprocess.run(["ip", "addr", "show", "tun0"], capture_output=True)
    if tun0_check.returncode == 0:
        # Get the IP address of tun0
        ip_address = subprocess.run(["ip", "-br", "addr", "show", "tun0"], capture_output=True, text=True)
        ip_address = ip_address.stdout.split()[2].split("/")[0]
    else:
        # Get the IP address of ens33 as fallback
        ip_address = subprocess.run(["ip", "-br", "addr", "show", "ens33"], capture_output=True, text=True)
        ip_address = ip_address.stdout.split()[2].split("/")[0]

    return ip_address


mod = "mod4"
terminal = "kitty"
keys = [
    # Switch between windows
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows in current stack.
    Key([mod, "shift"], "space", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", mod],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + group number = switch to & move focused window to group
            Key(
[mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )
colors = colors.Dracula


layouts = [
    layout.Spiral(margin=5,border_focus=colors[0],border_width=2,main_pane="top", clockwise=False),
    layout.Max(),
]

widget_defaults = dict(
    font="HackNerdFont",
    fontsize=15,
    padding=5,
    background=colors[2],
    margin_x=7,
    foreground=colors[1],
)
extension_defaults = widget_defaults.copy()
with open("/home/jotafab/.target_ip", "r") as f:
    target_ip = f.read().strip()

screens = [
    Screen(
        wallpaper='~/.config/qtile/background.jpg',
        wallpaper_mode='fill',
        top=bar.Bar(
            [
                #widget.CurrentLayout(),
                widget.GroupBox(highlight_color=colors[0],highlight_method='line',hide_unused=True),
                widget.Prompt(),
                widget.WindowTabs(),
                widget.TextBox(text = target_ip, foreground="ff0320", padding=10),
                widget.TextBox(text = get_ip_address(),foreground="00FF00",padding=10),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
            ],
            24,
            opacity=0.6,
            margin=[2,7,2,7],
            border_width=0,  # Draw top and bottom borders
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]



# Drag 
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
