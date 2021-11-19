import sys
import tkinter as tk
import pygame

from tileset_creator_src.options_frame import OptionsFrame
from tileset_creator_src.display import Display

pygame.init()
pygame.display.set_caption("Tileset Creator")
screen = pygame.display.set_mode((640, 640), pygame.RESIZABLE)
display = Display(screen)

window = tk.Tk()
options = OptionsFrame(window, display)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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
