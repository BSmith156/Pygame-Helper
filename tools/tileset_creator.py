import os
import sys
import tkinter as tk
import pygame

from tileset_creator.options_manager import OptionsManager
from tileset_creator.display_manager import DisplayManager
from tileset_creator.file_manager import FileManager

pygame.init()
pygame.display.set_caption("Tileset Creator")
icon_path = os.path.join(os.path.dirname(__file__), "tileset_creator/icon.png")
pygame.display.set_icon(pygame.image.load(icon_path))
screen = pygame.display.set_mode((640, 640), pygame.RESIZABLE)
window = tk.Tk()
window.tk.call('wm', 'iconphoto', window._w, tk.PhotoImage(file = icon_path))

display = DisplayManager(screen)
file_manager = FileManager()
options = OptionsManager(window, display, file_manager)
display.options = options

def check_saved():
    if options.check_saved():
        window.destroy()
window.protocol('WM_DELETE_WINDOW', check_saved)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if options.check_saved():
                pygame.quit()
                sys.exit()
        else:
            display.handle_event(event, options)
    display.update(options)
    pygame.display.update()
    try:
        window.update()
    except tk.TclError:
        pygame.quit()
        sys.exit()
