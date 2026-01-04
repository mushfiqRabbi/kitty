from kitty.boss import Boss

# import json
# class CustomEncoder(json.JSONEncoder):
#     def default(self, obj):
#         try:
#             return vars(obj)
#         except TypeError:
#             return str(obj)


def main(args: list[str]) -> str:
    pass

from kittens.tui.handler import result_handler
@result_handler(no_ui=True)
def handle_result(args: list[str], answer: str, target_window_id: int, boss: Boss) -> None:
    tab = boss.active_tab
    w = boss.window_id_map.get(target_window_id)

    # Detect if Shift+i was pressed (you'll need to configure kitty.conf to pass --new-tab)
    open_in_new_tab = "--new-tab" in args

    if open_in_new_tab:
        # Ctrl+A Shift+i: Open AI in a new tab
        if tab.title == "mvim" or tab.title == "nvim":
            boss.call_remote_control(w, ('send-key', 'Space', 'a', 'Shift+i'))
            return

        boss.call_remote_control(w, ('launch', '--type=tab', '--cwd=current', 'zsh', '-ic', 'mise x node@latest -- qwen'))
    else:
        # Ctrl+A i: Open AI in vertical split (original behavior)
        if tab.title == "mvim" or tab.title == "nvim":
            boss.call_remote_control(w, ('send-key', 'Space', 'a', 'i'))
            return

        boss.call_remote_control(w, ('goto-layout', 'splits'))
        boss.call_remote_control(w, ('launch', '--type=window', '--location=vsplit', '--bias=45', '--cwd=current', 'zsh', '-ic', 'mise x node@latest -- qwen'))
