import tkinter as tk

class ScrollableFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.canvas = tk.Canvas(self)
        self.frame = tk.Frame(self.canvas)
        self.vscroll = tk.Scrollbar(self, orient = "vertical", command = self.canvas.yview)
        self.hscroll = tk.Scrollbar(self, orient = "horizontal", command = self.canvas.xview)

        self.canvas.configure(yscrollcommand = self.vscroll.set)
        self.canvas.configure(xscrollcommand = self.hscroll.set)

        self.vscroll.pack(side = "left", fill = "y")
        self.hscroll.pack(side = "bottom", fill = "x")
        self.canvas.pack(side = "left", fill = "both", expand = True)
        self.canvas.create_window((0, 0), window = self.frame, anchor = "nw", tags = "self.frame")

        self.frame.bind("<Configure>", self.configure_callback)

    def configure_callback(self, e):
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
