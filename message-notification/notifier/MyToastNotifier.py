from win10toast import ToastNotifier
from win32gui import *
import time


class MyToastNotifier(ToastNotifier):

    def on_destroy(self, hwnd, msg, wparam, lparam):
        time.sleep(2)
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0)
