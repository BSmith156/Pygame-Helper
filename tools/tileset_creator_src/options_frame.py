import tkinter as tk
from tkinter.filedialog import askopenfilename

from helpers.screen_sizes import get_screen_size
from helpers.screen_sizes import get_title_bar_height

class OptionsFrame(tk.Frame):
    def __init__(self, master, display):
        super().__init__(master, bg="#252526")
        self._master = master
        self._display = display
        self.pack(fill=tk.BOTH, expand=1)

        menu_bar = tk.Menu(master)
        master.config(menu = menu_bar)

        master.title("Tileset Creator")
        screen_width, screen_height = get_screen_size()
        bar_height = get_title_bar_height()
        master.geometry("320x640+" + str(int(screen_width / 2 - 649)) + "+"
                        + str(int(screen_height / 2 - 320 - bar_height)))

        file_menu = tk.Menu(menu_bar, tearoff = 0)
        file_menu.add_command(label = "Open Tileset", command = self._menu_bar_open,
                              accelerator = "Ctrl+O")
        master.bind_all("<Control-o>", self._menu_bar_open)
        file_menu.add_separator()
        file_menu.add_command(label = "Save Tileset")
        file_menu.add_separator()
        file_menu.add_command(label = "Exit", command = self._menu_bar_exit)
        menu_bar.add_cascade(label = "File", menu = file_menu)

        view_menu = tk.Menu(menu_bar, tearoff = 0)
        view_menu.add_command(label = "Reset Offset", command = self._menu_bar_reset_offset)
        view_menu.add_command(label = "Reset Zoom", command = self._menu_bar_reset_zoom)
        view_menu.add_separator()
        view_menu.add_command(label = "Toggle Background", command = self._menu_bar_toggle_bg)
        menu_bar.add_cascade(label = "View", menu = view_menu)
        self._dark_bg = True

        self._current_path = ""

    @property
    def dark_bg(self):
        return self._dark_bg

    @property
    def current_path(self):
        return self._current_path

    def _menu_bar_exit(self):
        self._master.destroy()

    def _menu_bar_open(self, *args):
        path = askopenfilename(title='Open Tileset', filetypes=[("Image", ".png")])
        if path != "":
            self._current_path = path

    def _menu_bar_reset_offset(self):
        self._display.offset = [0, 0]

    def _menu_bar_reset_zoom(self):
        self._display.reset_zoom()

    def _menu_bar_toggle_bg(self):
        self._dark_bg = not self._dark_bg
