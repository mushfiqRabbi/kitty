# ~/.config/kitty/mywatcher.py
from typing import Any
from kitty.boss import Boss
from kitty.window import Window

import json
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return vars(obj)
        except TypeError:
            return str(obj)


full_screen_apps = {"nvim", "btop", "htop", "top", "lazygit", "lazydocker", "lg", "ld"}


def on_load(boss: Boss, data: dict[str, Any]) -> None:
    ...


def on_resize(boss: Boss, window: Window, data: dict[str, Any]) -> None:
    # print(json.dumps(data, indent=2, cls=CustomEncoder))
    print("running on_resize")

    # full_screen_apps = {"nvim", "btop", "htop", "top", "lazygit", "lazydocker", "lg", "ld", "kitty-scrollback.nvim"}
    tab = boss.active_tab
    layout_name = tab._current_layout_name
    window_count = len(tab.windows.all_windows)
    width = data['new_geometry'].right - data['new_geometry'].left
    height = data['new_geometry'].bottom - data['new_geometry'].top
    spaces_new = data['new_geometry'].spaces
    total_space_new = spaces_new.left + spaces_new.right + spaces_new.top + spaces_new.bottom
    padding_zero = (
        window.padding.left == 0 and
        window.padding.right == 0 and
        window.padding.top == 0 and
        window.padding.bottom == 0
    )

    padding_two = (
        window.padding.left == 2 and
        window.padding.right == 2 and
        window.padding.top == 2 and
        window.padding.bottom == 2
    )

    if any(window.title.lower().strip().startswith(app.lower().strip()) for app in full_screen_apps):
        if layout_name == "splits":
            if window_count > 1:
                if padding_zero:
                    boss.call_remote_control(window, ("set-spacing", f"padding=2"))
            else:
                if not padding_zero:
                    boss.call_remote_control(window, ("set-spacing", f"padding=0"))
        else:
            if not padding_zero:
                boss.call_remote_control(window, ("set-spacing", f"padding=0"))

        # padding = "2" if layout_name == "splits" and window_count > 1 else "0"
    else:
        if width <= 450 or height <= 300:
            if not padding_two:
                boss.call_remote_control(window, ('set-spacing', 'padding=2' ))
        elif width > 500 or height > 350:
            if padding_two:
                boss.call_remote_control(window, ('set-spacing', 'padding=default' ))
        # else:
        #     ...
        #     boss.call_remote_control(window, ('set-spacing', 'padding=default' ))

    # spaces_old = data['old_geometry'].spaces
    # total_space_old = spaces_old.left + spaces_old.right + spaces_old.top + spaces_old.bottom
    # spaces_new = data['new_geometry'].spaces
    # total_space_new = spaces_new.left + spaces_new.right + spaces_new.top + spaces_new.bottom
    # space_change = total_space_new - total_space_old
    # print("running on_resize")
    # tab = boss.active_tab
    # class CustomEncoder(json.JSONEncoder):
    #     def default(self, obj):
    #         try:
    #             return obj.__dict__  # Try to serialize object's __dict__
    #         except AttributeError:
    #             return str(obj)      # Fallback to string representation
    # print(tab._current_layout_name)
    # print(len(tab.windows.all_windows))
    # layout_name = tab._current_layout_name
    # window_count = len(tab.windows.all_windows)
    # width = data['new_geometry'].right - data['new_geometry'].left
    # height = data['new_geometry'].bottom - data['new_geometry'].top
    # print(f"width: {width}")
    # print(f"new space: {total_space_new}")
    # print(f"window: {window.title}")
    # print(f"space_change: {space_change}")
    # print(f"tab: {tab}")
    # print(f"layout: {layout}")
    # else:
    #     if width <= 450 and total_space_new > 50:
    #         boss.call_remote_control(window, ('set-spacing', 'padding=2' ))
        # elif width > 450 and total_space_new <= 50:
        #     boss.call_remote_control(window, ('set-spacing', 'padding=default' ))
        # else:
        #     ...
            # boss.call_remote_control(window, ('set-spacing', 'padding=default' ))

        # print(f"tab_layout : {boss.active_tab.current_layout.name}")
        # print(f"window title: {window.title}")
        # print(f"space_change: {space_change}")
        # print(total_space_new)
        # if space_change > 0:
        #     # if space_change >= 5:
        #     boss.call_remote_control(window, ('set-spacing', 'padding=2' ))
        #     # print(f"window: {window.title}")
        #     # print(f"space_change: {space_change}")
        #     # print(total_space_new)
        #     # boss.call_remote_control(window, ('set-spacing', 'padding=2' ))
        # else:
        #     boss.call_remote_control(window, ('set-spacing', 'padding=0' ))



def on_focus_change(boss: Boss, window: Window, data: dict[str, Any]) -> None:
    ...


def on_close(boss: Boss, window: Window, data: dict[str, Any]) -> None:
    ...


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
