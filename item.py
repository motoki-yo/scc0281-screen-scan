import ctypes
from commctrl import LVM_GETITEMCOUNT
import pywintypes
import win32gui
GetShellWindow = ctypes.windll.user32.GetShellWindow


def get_desktop():
    """Get the window of the icons, the desktop window contains this window"""
    shell_window = GetShellWindow()
    shell_dll_defview = win32gui.FindWindowEx(shell_window, 0, "SHELLDLL_DefView", "")
    if shell_dll_defview == 0:
        sys_listview_container = []
        try:
            win32gui.EnumWindows(_callback, sys_listview_container)
        except pywintypes.error as e:
            if e.winerror != 0:
                raise
        sys_listview = sys_listview_container[0]
    else:
        sys_listview = win32gui.FindWindowEx(shell_dll_defview, 0, "SysListView32", "FolderView")
    return sys_listview

def _callback(hwnd, extra):
    class_name = win32gui.GetClassName(hwnd)
    if class_name == "WorkerW":
        child = win32gui.FindWindowEx(hwnd, 0, "SHELLDLL_DefView", "")
        if child != 0:
            sys_listview = win32gui.FindWindowEx(child, 0, "SysListView32", "FolderView")
            extra.append(sys_listview)
            return False
    return True

def get_item_count(window):
    return win32gui.SendMessage(window, LVM_GETITEMCOUNT)

desktop = get_desktop()
get_item_count(desktop)

print(get_item_count(desktop))