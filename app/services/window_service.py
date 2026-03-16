from tkinter import Wm

def lock_window_size(window: Wm, width = 300):
    window.minsize(width, window.winfo_reqheight())
    window.maxsize(width, window.winfo_reqheight())

def center_window(window: Wm):
    x = (window.winfo_screenwidth() // 2) - (window.winfo_reqwidth() // 2)
    y = (window.winfo_screenheight() // 2) - (window.winfo_reqheight() // 2)
    window.geometry(f"+{x}+{y}")