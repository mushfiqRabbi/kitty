import os
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
    cwd = "--cwd-home" in args
    if tab.title == "nvim":
        boss.call_remote_control(w, ('goto-layout', 'splits'))
        boss.call_remote_control(w, ('launch', '--type=window', '--location=vsplit', '--bias=25', f"--cwd={os.path.expanduser("~") if cwd else "current"}"))
    else:
        boss.call_remote_control(w, ('goto-layout', 'splits'))
        boss.call_remote_control(w, ('launch', '--type=window', '--location=vsplit', '--bias=50', f"--cwd={os.path.expanduser("~") if cwd else "current"}"))

    # print(json.dumps(w, indent=2, cls=CustomEncoder))
