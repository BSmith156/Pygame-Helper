import tkinter as tk

class ScrollableFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg = "#333333", pady = 5)
        self.canvas = tk.Canvas(self, bg = "#333333", highlightthickness = 0)
        self.frame = tk.Frame(self.canvas, bg = "#333333")
        self.vscroll = tk.Scrollbar(self, orient = "vertical", command = self.canvas.yview,
                                    relief = tk.FLAT)

        self.canvas.configure(yscrollcommand = self.vscroll.set)

        self.vscroll.pack(side = "left", fill = "y")
        self.canvas.pack(side = "left", fill = "both", expand = True)
        self.canvas.create_window((0, 0), window = self.frame, anchor = "nw", tags = "self.frame")

        self.frame.bind("<Configure>", self.configure_callback)

    def configure_callback(self, e):
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
