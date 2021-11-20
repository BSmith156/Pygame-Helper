import math
import pygame

class DisplayManager():
    MIN_ZOOM = 1
    DARK_BG = (30, 30, 30)
    LIGHT_BG = (225, 225, 225)
    SELECT_COLOR = (25, 25, 25)

    def __init__(self, surf):
        self.surf = surf
        self.img = None
        self.dragging = False
        self.mouse_prev = None
        self.select_start = None

    def set_img(self, path):
        self.img = pygame.image.load(path)
        self.set_colorkey(None, False)
        self.offset = [0, 0]
        self.reset_zoom()

    def set_colorkey(self, colorkey, update_zoom = True):
        if colorkey is None:
            self.colorkey_img = self.img.convert_alpha()
        else:
            self.colorkey_img = self.img.convert()
            self.colorkey_img.set_colorkey(colorkey)
        if update_zoom:
            self.update_zoom()

    def update_zoom(self):
        self.zoom_img = pygame.transform.scale(self.colorkey_img,
                                              (self.img.get_width() * self.zoom,
                                               self.img.get_height() * self.zoom))

    def reset_zoom(self):
        x_zoom = self.surf.get_width() / self.img.get_width()
        y_zoom = self.surf.get_height() / self.img.get_height()
        self.zoom = round(min(x_zoom, y_zoom))
        self.zoom = max(self.zoom, DisplayManager.MIN_ZOOM)
        self.update_zoom()

    def pos_to_pixel(self, pos):
        return (math.floor((pos[0] / self.zoom) - (self.offset[0] / self.zoom)),
                math.floor((pos[1] / self.zoom) - (self.offset[1] / self.zoom)))

    def handle_event(self, event, options_manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.img is not None:
                self.dragging = False
                self.select_start = self.pos_to_pixel(pygame.mouse.get_pos())
                if self.select_start[0] < 0 or self.select_start[1] < 0:
                    self.select_start = None
                elif self.select_start[0] >= self.img.get_width() or self.select_start[1] >= self.img.get_height():
                    self.select_start = None

            elif event.button == 3 and self.img is not None and self.select_start is None:
                self.dragging = True

            elif event.button == 4 and self.img is not None:
                self.zoom = round(self.zoom + 1)
                self.update_zoom()

            elif event.button == 5 and self.img is not None:
                self.zoom = round(self.zoom - 1)
                self.zoom = max(self.zoom, DisplayManager.MIN_ZOOM)
                self.update_zoom()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.select_start is not None:
                options_manager.selection(self.selection)
                self.select_start = None

            if event.button == 3:
                self.dragging = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                options_manager.save_file()

    def update(self, options_manager):
        if self.dragging:
            if self.mouse_prev is None:
                self.mouse_prev = pygame.mouse.get_pos()
            else:
                self.offset[0] += pygame.mouse.get_pos()[0] - self.mouse_prev[0]
                self.offset[1] += pygame.mouse.get_pos()[1] - self.mouse_prev[1]
                self.mouse_prev = pygame.mouse.get_pos()
        else:
            self.mouse_prev = None

        if options_manager.is_dark_bg:
            self.surf.fill(DisplayManager.DARK_BG)
        else:
            self.surf.fill(DisplayManager.LIGHT_BG)

        if self.img is not None:
            self.surf.blit(self.zoom_img, self.offset)

        if self.select_start is not None:
            select_end = self.pos_to_pixel(pygame.mouse.get_pos())
            select_end = (max(min(select_end[0], self.img.get_width() - 1), 0),
                          max(min(select_end[1], self.img.get_height() - 1), 0))

            select_x = min(self.select_start[0], select_end[0])
            select_y = min(self.select_start[1], select_end[1])
            select_w = abs(self.select_start[0] - select_end[0]) + 1
            select_h = abs(self.select_start[1] - select_end[1]) + 1
            self.selection = (select_x, select_y, select_w, select_h)

            select_box = pygame.Surface((select_w * self.zoom, select_h * self.zoom))
            select_box.fill(DisplayManager.SELECT_COLOR)
            self.surf.blit(select_box, (select_x * self.zoom + self.offset[0],
                                        select_y * self.zoom + self.offset[1]),
                           special_flags = pygame.BLEND_ADD)
