import tkinter as tk

class OptionsMenu(tk.Menu):
    def __init__(self, master, options_manager):
        super().__init__(master)
        self.master = master
        self.options_manager = options_manager
        master.config(menu = self)

    def create_menus(self):
        file_menu = tk.Menu(self, tearoff = 0)
        file_menu.add_command(label = "Open Tileset", command = self.options_manager.open_file)
        file_menu.add_separator()

        file_menu.add_command(label = "Save Tileset", command = self.options_manager.save_file,
                              accelerator = "Ctrl+S")
        self.master.bind_all("<Control-s>", self.options_manager.save_file)
        file_menu.add_separator()

        file_menu.add_command(label = "Exit", command = self.options_manager.exit)

        self.add_cascade(label = "File", menu = file_menu)

        view_menu = tk.Menu(self, tearoff = 0)
        view_menu.add_command(label = "Reset Offset", command = self.options_manager.reset_offset)

        view_menu.add_command(label = "Reset Zoom", command = self.options_manager.reset_zoom)
        view_menu.add_separator()

        view_menu.add_command(label = "Toggle Background", command = self.options_manager.toggle_bg)

        self.add_cascade(label = "View", menu = view_menu)
