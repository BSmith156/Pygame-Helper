import tkinter as tk

class ColorkeyFrame(tk.LabelFrame):
    def __init__(self, options_manager, display_manager, file_manager):
        super().__init__(options_manager, text = "Colour Key")
        self.options_manager = options_manager
        self.display_manager = display_manager
        self.file_manager = file_manager
        self.pack(fill = tk.X, side = tk.TOP)
        self.create_widgets()

    def create_widgets(self):
        self.is_colorkey = tk.IntVar()
        self.checkbox = tk.Checkbutton(self, text = "Use Colour Key",
                                       variable = self.is_colorkey, onvalue = 1,
                                       offvalue = 0, command = self.update_colorkey,
                                       state = tk.DISABLED)
        self.checkbox.pack(anchor = tk.W)

        color_frame = tk.Frame(self)
        color_frame.pack(anchor = tk.W)

        self.colors = []
        for i in range(3):
            self.colors.append(tk.Entry(color_frame))
            self.colors[i].pack(side = tk.LEFT)

        self.button = tk.Button(self, text = "Set Colour Key",
                                command = self.update_colorkey, state = tk.DISABLED)
        self.button.pack(anchor = tk.W)
        self.disable_colors()

    def disable_colors(self, reset_values = True):
        for color in self.colors:
            if reset_values:
                color.config(state = tk.NORMAL)
                color.delete(0, tk.END)
                color.insert(tk.END, "0")
            color.config(state = tk.DISABLED)
        self.button.config(state = tk.DISABLED)

    def set_colors(self, color):
        for i in range(3):
            self.colors[i].config(state = tk.NORMAL)
            self.colors[i].delete(0, tk.END)
            self.colors[i].insert(tk.END, str(color[i]))
        self.button.config(state = tk.NORMAL)
    
    def update_colorkey(self):
        if self.is_colorkey.get():
            new_color = []
            for color in self.colors:
                try:
                    new_color.append(int(color.get()))
                    new_color[-1] = max(min(new_color[-1], 255), 0)
                except ValueError:
                    new_color.append(0)
            self.display_manager.set_colorkey(new_color)
            self.file_manager.data["colorkey"] = new_color
            self.file_manager.unsaved = True
            self.set_colors(new_color)
        else:
            self.display_manager.set_colorkey(None)
            self.file_manager.data["colorkey"] = False
            self.file_manager.unsaved = True
            self.disable_colors(False)
