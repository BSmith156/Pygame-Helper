import tkinter as tk

from tkinter import simpledialog
from tkinter import messagebox
from tkinter.font import Font

from tileset_creator.scrollable_frame import ScrollableFrame

class TilesFrame(tk.LabelFrame):
    def __init__(self, master, display_manager, file_manager):
        super().__init__(master, text = "Tiles", bg = "#333333",
                         fg = "#e8e8e8", relief = tk.FLAT,
                         font = Font(size = 15, weight = "bold", underline = True),
                         padx = 5)
        self.display_manager = display_manager
        self.file_manager = file_manager
        self.pack(fill = tk.BOTH, side = tk.BOTTOM, expand = True)

        self.tiles_list = ScrollableFrame(self)
        self.tiles_list.pack(fill = tk.BOTH, expand = True)

        self.tile_menu = tk.Menu(self.winfo_toplevel(), tearoff = False)
        self.tile_menu.add_command(label = "Rename Tile", command = self.rename_tile)
        self.tile_menu.add_command(label = "Delete Tile", command = self.delete_tile)

        self.clicked_tile = None

    def update(self, new_tiles):
        for widget in self.tiles_list.frame.winfo_children():
            widget.destroy()
        for tile in new_tiles:
            if self.clicked_tile == tile[0]:
                font_color = "#e8e8e8"
                font_weight = "bold"
            else:
                font_color = "#a7a8a9"
                font_weight = "normal"
            tile_text = tk.Label(self.tiles_list.frame, text = tile[0], bg = "#333333",
                                 fg = font_color, font = Font(size = 10, weight = font_weight))
            tile_text.bind("<Button-1>", self.tile_click)
            tile_text.bind("<Button-3>", self.tile_right_click)
            tile_text.pack(anchor = tk.W)

    def tile_click(self, event):
        tile_name = event.widget.cget("text")
        if self.clicked_tile == tile_name:
            self.display_manager.unshow_tile()
            self.clicked_tile = None
        else:
            for tile in self.file_manager.data["tiles"]:
                if tile[0] == tile_name:
                    self.display_manager.show_tile(tile[1])
                    self.clicked_tile = tile_name
                    break
        self.update(self.file_manager.data["tiles"])

    def tile_right_click(self, event):
        try:
            self.right_clicked_tile = event.widget.cget("text")
            self.tile_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.tile_menu.grab_release()

    def delete_tile(self):
        for tile in self.file_manager.data["tiles"]:
            if tile[0] == self.right_clicked_tile:
                self.file_manager.data["tiles"].remove(tile)
                self.file_manager.data["tiles"].sort()
                self.file_manager.unsaved = True
                self.update(self.file_manager.data["tiles"])
                if tile[0] == self.clicked_tile:
                    self.display_manager.unshow_tile()
                    self.clicked_tile = None
                break

    def rename_tile(self):
        msg = "New tile name:"
        while True:
            tile_name = simpledialog.askstring("Rename Tile", msg,
                                            parent=self.master)
            if tile_name == "":
                msg = "Tile name can't be blank!"
                continue
            cont = False
            for tile in self.file_manager.data["tiles"]:
                if tile_name == tile[0]:
                    msg = "New tile name:"
                    if not messagebox.askyesno("Tile Already Exists!", "Overwrite tile?"):
                        cont = True
                    elif tile_name != self.right_clicked_tile:
                        self.file_manager.data["tiles"].remove(tile)
                    break
            if cont:
                continue
            break

        if tile_name is not None and tile_name != self.right_clicked_tile:
            for tile in self.file_manager.data["tiles"]:
                if tile[0] == self.right_clicked_tile:
                    if tile[0] == self.clicked_tile:
                        self.clicked_tile = tile_name
                    tile[0] = tile_name
                    break
            self.file_manager.data["tiles"].sort()
            self.file_manager.unsaved = True
            self.update(self.file_manager.data["tiles"])
