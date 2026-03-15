from tkinter import Wm

def lock_window_size(window: Wm, width = 300):
    window.update_idletasks() # Ne fait pas partie de Wm mais fonctionne quand même
    window.minsize(width, window.winfo_reqheight())
    window.maxsize(width, window.winfo_reqheight())