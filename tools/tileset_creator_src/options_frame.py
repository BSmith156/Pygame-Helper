import tkinter as tk
from tkinter.filedialog import askopenfilename

from helpers.screen_sizes import get_screen_size
from helpers.screen_sizes import get_title_bar_height

class OptionsFrame(tk.Frame):
    def __init__(self, master, display):
        super().__init__(master)
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
        
        colorkey_frame = tk.LabelFrame(self, text = "Colour Key")
        colorkey_frame.pack(fill = tk.X, side = tk.TOP)

        self._is_colorkey = tk.IntVar()
        self._colorkey_check = tk.Checkbutton(colorkey_frame, text = "Use Colour Key",
                                              variable = self._is_colorkey, onvalue = 1,
                                              offvalue = 0, command = self._colorkey_cmd,
                                              state = tk.DISABLED)
        self._colorkey_check.pack(anchor = tk.W)

        colorkey_color = tk.Frame(colorkey_frame)
        colorkey_color.pack(anchor = tk.W)

        self._colorkey_red = tk.Entry(colorkey_color)
        self._colorkey_red.pack(side = tk.LEFT)
        self._colorkey_red.insert(tk.END, "0")
        self._colorkey_red.config(state = tk.DISABLED)
        self._colorkey_green = tk.Entry(colorkey_color)
        self._colorkey_green.pack(side = tk.LEFT)
        self._colorkey_green.insert(tk.END, "0")
        self._colorkey_green.config(state = tk.DISABLED)
        self._colorkey_blue = tk.Entry(colorkey_color)
        self._colorkey_blue.pack(side = tk.LEFT)
        self._colorkey_blue.insert(tk.END, "0")
        self._colorkey_blue.config(state = tk.DISABLED)

        self._colorkey_button = tk.Button(colorkey_frame, text = "Set Colour Key",
                                          command = self._colorkey_cmd, state = tk.DISABLED)
        self._colorkey_button.pack(anchor = tk.W)

        tiles_frame = tk.LabelFrame(self, text = "Tiles")
        tiles_frame.pack(fill = tk.BOTH, side = tk.BOTTOM, expand = True)

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
            self._colorkey_check.config(state = tk.NORMAL)

    def _menu_bar_reset_offset(self):
        self._display.offset = [0, 0]

    def _menu_bar_reset_zoom(self):
        self._display.reset_zoom()

    def _menu_bar_toggle_bg(self):
        self._dark_bg = not self._dark_bg
  
    def _colorkey_cmd(self):
        if self._is_colorkey.get():
            try:
                red = int(self._colorkey_red.get())
                red = max(min(red, 255), 0)
            except ValueError:
                red = 0
            try:
                green = int(self._colorkey_green.get())
                green = max(min(green, 255), 0)
            except ValueError:
                green = 0
            try:
                blue = int(self._colorkey_blue.get())
                blue = max(min(blue, 255), 0)
            except ValueError:
                blue = 0
            self._display.colorkey = ((red, green, blue))
            self._colorkey_red.config(state = tk.NORMAL)
            self._colorkey_red.delete(0, tk.END)
            self._colorkey_red.insert(tk.END, str(red))
            self._colorkey_green.config(state = tk.NORMAL)
            self._colorkey_green.delete(0, tk.END)
            self._colorkey_green.insert(tk.END, str(green))
            self._colorkey_blue.config(state = tk.NORMAL)
            self._colorkey_blue.delete(0, tk.END)
            self._colorkey_blue.insert(tk.END, str(blue))
            self._colorkey_button.config(state = tk.NORMAL)
        else:
            self._display.colorkey = None
            self._colorkey_red.config(state = tk.DISABLED)
            self._colorkey_green.config(state = tk.DISABLED)
            self._colorkey_blue.config(state = tk.DISABLED)
            self._colorkey_button.config(state = tk.DISABLED)
