import json
import os
import pygame

class TilesetManager():
    def __init__(self):
        self._tilesets = {}

    def load(self, path):
        for filename in os.listdir(path):
            split = filename.split("_")
            if split[-1] != "config.json":
                continue
            with open(path + "/" + filename, "r", encoding="utf-8") as config_file:
                config = json.loads(config_file.read())
            tileset = "_".join(split[:-1])
            self._tilesets[tileset] = {}
            colorkey = config["colorkey"]
            image = pygame.image.load(path + "/" + tileset + ".png")
            if not colorkey:
                image = image.convert_alpha()
            else:
                image = image.convert()
                image.set_colorkey(colorkey)
            for tile in config["tiles"]:
                self._tilesets[tileset][tile[0]] = image.subsurface((tile[1][0], tile[1][1],
                                                                     tile[1][2], tile[1][3])).copy()

    def get_tileset(self, tileset):
        return self._tilesets[tileset]

    def get_tile(self, tileset, tile):
        return self._tilesets[tileset][tile]
