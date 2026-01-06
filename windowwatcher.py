# ~/.config/kitty/mywatcher.py
from typing import Any
# import json
from kitty.boss import Boss
from kitty.window import Window

# import json
# class CustomEncoder(json.JSONEncoder):
#     def default(self, obj):
#         try:
#             return vars(obj)
#         except TypeError:
#             return str(obj)


full_screen_apps = {"btop", "htop", "lazydocker", "lazygit", "ld", "lg", "mvim", "nvim", "top", "y", "yazi"}


def on_load(boss: Boss, data: dict[str, Any]) -> None:
    ...


last_padding_state: dict[int, str] = {}

def on_resize(boss: Boss, window: Window, data: dict[str, Any]) -> None:
    # print(json.dumps(data, indent=2, cls=CustomEncoder))
    print("running on_resize")

    old_width = (data['old_geometry'].right - data['old_geometry'].left) + (data['old_geometry'].spaces.left + data['old_geometry'].spaces.right)
    old_height = (data['old_geometry'].bottom - data['old_geometry'].top) + (data['old_geometry'].spaces.top + data['old_geometry'].spaces.bottom)
    new_width = (data['new_geometry'].right - data['new_geometry'].left) + (data['new_geometry'].spaces.left + data['new_geometry'].spaces.right)
    new_height = (data['new_geometry'].bottom - data['new_geometry'].top) + (data['new_geometry'].spaces.top + data['new_geometry'].spaces.bottom)

    if old_width == new_width and old_height == new_height:
        return

    tab = boss.active_tab
    layout_name = tab._current_layout_name
    window_count = len(tab.windows.all_windows)

    is_full_screen_app = any(window.title.lower().strip().startswith(app.lower()) for app in full_screen_apps)

    if is_full_screen_app:
        if layout_name == "splits":
            new_padding = "2" if window_count > 1 else "0"
        else:
            new_padding = "0"
    else:
        if new_width <= 500 or new_height <= 350:
            new_padding = "2"
        else:
            new_padding = "default"

    last_padding = last_padding_state.get(window.id)

    if last_padding != new_padding:
        boss.call_remote_control(window, ("set-spacing", f"padding={new_padding}"))
        last_padding_state[window.id] = new_padding


def on_focus_change(boss: Boss, window: Window, data: dict[str, Any]) -> None:
    ...


def on_close(boss: Boss, window: Window, data: dict[str, Any]) -> None:
    print("running on_close")

    last_padding_state.pop(window.id, None)


def on_set_user_var(boss: Boss, window: Window, data: dict[str, Any]) -> None:
    print("running on_set_user_var")

    if data.get('key') == 'in_ksb':
        raw_value = data.get('value')
        if raw_value is not None:
            boss.call_remote_control(window, ("set-colors", f"cursor=#ff757f"))
            boss.call_remote_control(window, ("set-colors", f"cursor_text_color=#1b1d2b"))


def on_title_change(boss: Boss, window: Window, data: dict[str, Any]) -> None:
    ...


def on_cmd_startstop(boss: Boss, window: Window, data: dict[str, Any]) -> None:
    print("running on_cmd_startstop")

    # full_screen_apps = {"nvim", "btop", "htop", "top", "lazygit", "lazydocker", "lg", "ld", "kitty-scrollback.nvim"}
    cmd = data["cmdline"]
    is_start = data["is_start"]
    if any(cmd.lower().strip().startswith(app.lower().strip()) for app in full_screen_apps):
        if is_start:
            tab = boss.active_tab
            layout_name = tab._current_layout_name
            window_count = len(tab.windows.all_windows)

            padding = "2" if layout_name == "splits" and window_count > 1 else "0"
        else:
            padding = "default"

        boss.call_remote_control(window, ("set-spacing", f"padding={padding}"))


def on_color_scheme_preference_change(boss: Boss, window: Window, data: dict[str, Any]) -> None:
    ...
