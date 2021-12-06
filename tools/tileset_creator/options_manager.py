from sys import platform

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog
from tkinter import messagebox

from tileset_creator.options_menu import OptionsMenu
from tileset_creator.colorkey_frame import ColorkeyFrame
from tileset_creator.tiles_frame import TilesFrame

class OptionsManager(tk.Frame):
    def __init__(self, master, display_manager, file_manager):
        super().__init__(master, bg = "#333333")
        self.master = master
        self.display_manager = display_manager
        self.file_manager = file_manager
        self.pack(fill=tk.BOTH, expand=1)

        options_menu = OptionsMenu(master, self)

        master.title("Tileset Creator")
        screen_size = get_screen_size()
        master.geometry("320x640+" + str(int(screen_size[0] / 2 - 649)) + "+"
                        + str(int(screen_size[1] / 2 - 320 - get_title_bar_height())))

        options_menu.create_menus()

        self.colorkey_frame = ColorkeyFrame(self, display_manager, file_manager)

        self.tiles_frame = TilesFrame(self, display_manager, file_manager)

        self.current_path = ""
        self.is_dark_bg = True

    def open_file(self, *args):
        path = askopenfilename(title='Open Tileset', filetypes=[("Image", ".png")])
        if path != "":
            if not self.check_saved():
                return

            self.current_path = path

            self.display_manager.set_img(self.current_path)

            name = ''.join(path.split('.')[:-1]) + "_config.json"
            self.file_manager.load_data(name)

            self.colorkey_frame.checkbox.config(state = tk.NORMAL)
            self.colorkey_frame.checkbox_label.config(fg = "#e8e8e8")
            if not self.file_manager.data["colorkey"]:
                self.colorkey_frame.checkbox.deselect()
                self.display_manager.set_colorkey(None)
                self.colorkey_frame.disable_colors()
            else:
                color = self.file_manager.data["colorkey"]
                self.colorkey_frame.checkbox.select()
                self.colorkey_frame.set_colors(color)
                self.display_manager.set_colorkey((color[0], color[1], color[2]))

            self.tiles_frame.update(self.file_manager.data["tiles"])

    def save_file(self, *args):
        name = ''.join(self.current_path.split('.')[:-1]) + "_config.json"
        self.file_manager.save_data(name)

    def reset_offset(self):
        self.display_manager.offset = [0, 0]

    def reset_zoom(self):
        self.display_manager.reset_zoom()

    def toggle_bg(self):
        self.is_dark_bg = not self.is_dark_bg

    def exit(self):
        if not self.check_saved():
            return
        self.master.destroy()

    def selection(self, selection):
        msg = "Tile name:"
        while True:
            tile_name = simpledialog.askstring("Create Tile", msg,
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
                    else:
                        self.file_manager.data["tiles"].remove(tile)
                    break
            if cont:
                continue
            break

        if tile_name is not None:
            self.file_manager.data["tiles"].append([tile_name, list(selection)])
            self.file_manager.data["tiles"].sort()
            self.file_manager.unsaved = True
            self.tiles_frame.update(self.file_manager.data["tiles"])
            if self.tiles_frame.clicked_tile == tile_name:
                self.display_manager.show_tile(list(selection))

    def check_saved(self):
        if self.file_manager.unsaved:
            save = messagebox.askyesnocancel("Unsaved Changes", "Save changes?")
            if save is None:
                return False
            if save:
                self.save_file()
        return True

def get_screen_size():
    root = tk.Tk()
    root.update_idletasks()
    root.attributes('-fullscreen', True)
    root.state('iconic')
    height = root.winfo_screenheight()
    width = root.winfo_screenwidth()
    root.destroy()
    return (width, height)

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
