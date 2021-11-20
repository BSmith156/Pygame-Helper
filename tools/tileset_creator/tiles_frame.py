import tkinter as tk

from tileset_creator.scrollable_frame import ScrollableFrame

class TilesFrame(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text = "Tiles")
        self.pack(fill = tk.BOTH, side = tk.BOTTOM, expand = True)

        self.tiles_list = ScrollableFrame(self)
        self.tiles_list.pack(fill = tk.BOTH, expand = True)
    
    def update(self, new_tiles):
        for tile in self.tiles_list.frame.winfo_children():
            tile.destroy()
        for tile in new_tiles:
            tile_text = tk.Label(self.tiles_list.frame, text = tile[0])
            tile_text.pack(anchor = tk.W)
            