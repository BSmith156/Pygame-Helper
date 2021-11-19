import sys
import tkinter as tk
import pygame

from tileset_creator_src.options_frame import OptionsFrame
from tileset_creator_src.display import Display
from tileset_creator_src.file_manager import FileManager

pygame.init()
pygame.display.set_caption("Tileset Creator")
screen = pygame.display.set_mode((640, 640), pygame.RESIZABLE)
display = Display(screen)

file_manager = FileManager()

window = tk.Tk()
options = OptionsFrame(window, display, file_manager)
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
            display.handle_event(event)
    display.update(options)
    pygame.display.update()
    try:
        window.update()
    except tk.TclError:
        pygame.quit()
        sys.exit()
