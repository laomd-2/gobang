from win10toast import ToastNotifier
from win32gui import *
import random


class MyToastNotifier(ToastNotifier):

    def on_destroy(self, hwnd, msg, wparam, lparam):
        PostQuitMessage(0)