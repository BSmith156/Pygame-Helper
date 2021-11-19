from sys import platform
import tkinter as tk

def get_screen_size():
    root = tk.Tk()
    root.update_idletasks()
    root.attributes('-fullscreen', True)
    root.state('iconic')
    height = root.winfo_screenheight()
    width = root.winfo_screenwidth()
    root.destroy()
    return width, height

def get_title_bar_height():
    root = tk.Tk()
    root.update_idletasks()
    offset_y = 0
    if platform in ('win32', 'darwin'):
        import ctypes
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except:
            ctypes.windll.user32.SetProcessDPIAware()
        offset_y = int(root.geometry().rsplit('+', 1)[-1])

    bar_height = root.winfo_rooty() - offset_y
    root.destroy()
    return bar_height
