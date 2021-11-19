import pygame

from helpers.pixels import get_pixel

class Display():
    def __init__(self, screen):
        self._screen = screen
        self._path = ""
        self._offset = [0, 0]
        self._zoom = 1
        self._right_click = False
        self._last_right = None
        self._box_top_left = None

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, new_offset):
        self._offset = new_offset

    @property
    def colorkey(self):
        return self._colorkey

    @colorkey.setter
    def colorkey(self, new_colorkey):
        self._colorkey = new_colorkey
        if new_colorkey is None:
            self._display_image = self._image.copy().convert_alpha()
        else:
            self._display_image = self._image.copy().convert()
            self._display_image.set_colorkey(new_colorkey)
        self._set_zoomed_image()

    def reset_zoom(self):
        x_scale = self._screen.get_width() / self._image.get_width()
        y_scale = self._screen.get_height() / self._image.get_height()
        self._zoom = round(min(x_scale, y_scale))
        self._zoom = max(self._zoom, 1)
        self._set_zoomed_image()

    def _set_zoomed_image(self):
        self._zoomed_image = pygame.transform.scale(self._display_image,
                             (self._image.get_width() * self._zoom,
                             self._image.get_height() * self._zoom))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._right_click = False
                self._box_top_left = get_pixel(pygame.mouse.get_pos(), self._offset, self._zoom)
            if event.button == 3 and self._box_top_left is None:
                self._right_click = True
            elif event.button == 4:
                self._zoom = round(self._zoom + 1)
                self._set_zoomed_image()
            elif event.button == 5:
                self._zoom = round(self._zoom - 1)
                self._zoom = max(self._zoom, 1)
                self._set_zoomed_image()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self._box_top_left is not None:
                self._box_top_left = None
            if event.button == 3:
                self._right_click = False

    def update(self, options_frame):
        if self._right_click:
            if self._last_right is None:
                self._last_right = pygame.mouse.get_pos()
            else:
                self._offset[0] += pygame.mouse.get_pos()[0] - self._last_right[0]
                self._offset[1] += pygame.mouse.get_pos()[1] - self._last_right[1]
                self._last_right = pygame.mouse.get_pos()
        else:
            self._last_right = None

        if options_frame.dark_bg:
            self._screen.fill((30, 30, 30))
        else:
            self._screen.fill((225, 225, 225))

        if self._path is not options_frame.current_path:
            self._path = options_frame.current_path
            self._image = pygame.image.load(self._path)
            self.colorkey = None
            self.reset_zoom()
            self._offset = [0, 0]
        if self._path != "":
            self._screen.blit(self._zoomed_image, self._offset)
        
        if self._box_top_left is not None:
            current_pos = get_pixel(pygame.mouse.get_pos(), self._offset, self._zoom)
            x_pos = min(self._box_top_left[0], current_pos[0])
            y_pos = min(self._box_top_left[1], current_pos[1])
            width = abs(self._box_top_left[0] - current_pos[0]) + 1
            height = abs(self._box_top_left[1] - current_pos[1]) + 1
            box = pygame.Surface((width * self._zoom, height * self._zoom))
            box.fill((25, 25, 25))
            self._screen.blit(box, (x_pos * self._zoom + self._offset[0],
                                    y_pos * self._zoom + self._offset[1]),
                                    special_flags = pygame.BLEND_ADD)
