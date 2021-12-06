import tkinter as tk

from tkinter.font import Font

class ColorkeyFrame(tk.LabelFrame):
    def __init__(self, options_manager, display_manager, file_manager):
        super().__init__(options_manager, text = "Colour Key", bg = "#333333",
                         fg = "#e8e8e8", relief = tk.FLAT,
                         font = Font(size = 15, weight = "bold", underline = True),
                         padx = 5, pady = 5)
        self.options_manager = options_manager
        self.display_manager = display_manager
        self.file_manager = file_manager
        self.pack(fill = tk.X, side = tk.TOP, pady = 5)
        self.create_widgets()

    def create_widgets(self):
        checkbox_frame = tk.Frame(self, bg = "#333333")
        checkbox_frame.pack(anchor = tk.W)

        self.is_colorkey = tk.IntVar()
        self.checkbox = tk.Checkbutton(checkbox_frame, variable = self.is_colorkey,
                                       onvalue = 1, offvalue = 0,
                                       command = self.update_colorkey, state = tk.DISABLED,
                                       bg = "#333333", relief = tk.FLAT, bd = 0, padx = 0,
                                       activebackground = "#333333", highlightthickness = 0)
        self.checkbox.pack(side = tk.LEFT)

        self.checkbox_label = tk.Label(checkbox_frame, text = "Use Colour Key", bg = "#333333",
                                       fg = "#a7a8a9", font = Font(size = 10), bd = 0, padx = 0)
        self.checkbox_label.pack(side = tk.LEFT)

        color_frame = tk.Frame(self, bg = "#333333")
        color_frame.pack(anchor = tk.W, pady = (5, 5), fill = tk.X)

        self.colors = []
        for i in range(3):
            self.colors.append(tk.Entry(color_frame, relief = tk.FLAT, bg = "#e8e8e8",
                                        disabledbackground = "#a7a8a9"))
            if i != 2:
                right_pad = 3
            else:
                right_pad = 0
            self.colors[i].grid(row = 0, column = i, sticky = "WE", padx = (0, right_pad))
            color_frame.grid_columnconfigure(i, weight = 1)

        self.button = tk.Button(self, text = "Set Colour Key",
                                command = self.update_colorkey, state = tk.DISABLED,
                                relief = tk.FLAT, bg = "#a7a8a9")
        self.button.pack(anchor = tk.W)
        self.disable_colors()

    def disable_colors(self, reset_values = True):
        for color in self.colors:
            if reset_values:
                color.config(state = tk.NORMAL)
                color.delete(0, tk.END)
                color.insert(tk.END, "0")
            color.config(state = tk.DISABLED)
        self.button.config(state = tk.DISABLED, bg = "#a7a8a9")

    def set_colors(self, color):
        for i in range(3):
            self.colors[i].config(state = tk.NORMAL)
            self.colors[i].delete(0, tk.END)
            self.colors[i].insert(tk.END, str(color[i]))
        self.button.config(state = tk.NORMAL, bg = "#e8e8e8")

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
